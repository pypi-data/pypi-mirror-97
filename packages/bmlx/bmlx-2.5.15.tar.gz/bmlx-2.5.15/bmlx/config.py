"""
配置模块，这个是一个相对通用的处理各种配置文件的方式，我们希望达到以下几个效果
1. 保证有序，传统的pyyaml模块，读取之后再序列化是会导致乱序的，这个在配置文件生成的时候会导致逻辑不太清晰
2. 可以任意维度覆盖，但是不能超过template的范畴，这样有两个好处，第一是下游可以直接通过attributedict方式访问，不用无休止的
if kw in dict:
dict.get(kw, default=xxx)
这种方式去处理配置，上述几种方式，都会导致代码可读性不好，另外配置的默认值，散落到代码里面，是一个非常不好的习惯

但是覆盖有一个比较棘手的问题 -- 到底覆盖到什么级别?
比如bmlx.yml里面，参数的配置，肯定应该是由用户自己来设置，default.config里面
```
parameters:
    hyper:
        learning_rate: 0.0001
```
如果用户希望增加一个参数，user.config里面看起来是
```
parameters:
    hyper:
        batch: 1024
```
那这个时候，config模块就比较懵了，最主要问题他不知道什么是merge级别，上面这个例子是二级的例子，如果我们设置merge keys级别为1，那learning_rate这个参数就会丢失
所以更合理的方式应该是由用户来动态的决定获取的级别，转为用户态去动态merge
比如上面这个例子
config["parameters"].get() -> 代表完全使用用户态的配置，合并级别为1, ret-> {"hpyer": {"batch": 1}}
config["parameters"]["hpyer"].get() -> 合并级别为2，ret-> {"hyper": {"batch": 1, "learning_rate": 0.0001}}

3. 类型的检查，配置大致有str, int, float, map, choice, list等类型，从配置性上，我们希望能够实现required或者optional, 我们希望在这层，能够定义清楚每个数据的范围（类似于xml的xsl）

这段代码结构是从 https://github.com/beetbox/confuse 摘抄过来的，根据我们需求进行过裁剪和修改
"""
import yaml
import pathlib
import urllib
import abc
import os
import sys
import re
import collections
import pkgutil
import enum
from typing import Text, Dict, Any, Optional
from string import Template as StrTemplate
from bmlx.utils.unit_utils import StorageUnit as StorageUnitModel

from collections import OrderedDict

_ROOT_NAME = "root"


class ConfigError(Exception):
    pass


class NotFoundError(ConfigError):
    pass


class ConfigValueError(ConfigError):
    pass


class ConfigTypeError(ConfigValueError):
    pass


class ConfigTemplateError(ConfigError):
    pass


def iter_first(sequence):
    it = iter(sequence)
    try:
        return next(it)
    except StopIteration:
        raise ValueError()


class ConfigSource(dict):
    def __init__(self, value, filename=None, default=False):
        super(ConfigSource, self).__init__(value)
        if filename is not None and not isinstance(filename, str):
            raise TypeError(u"filename must be a string or None")
        self.filename = filename
        self.default = default

    def __repr__(self):
        return "ConfigSource({0!r}, {1!r}, {2!r})".format(
            super(ConfigSource, self), self.filename, self.default,
        )

    @classmethod
    def of(cls, value):
        if isinstance(value, ConfigSource):
            return value
        elif isinstance(value, dict):
            return ConfigSource(value)
        else:
            raise TypeError(u"source value must be a dict")


class ConfigView(object):
    name = None

    _relatives = {}

    def __init__(self, relatives={}, value_converter=None):
        self._relatives = relatives
        self.value_converter = value_converter

    @property
    def relatives(self):
        return self._relatives

    @relatives.setter
    def relatives(self, value):
        if not isinstance(value, dict):
            raise TypeError("'relatives' must be map")
        self._relatives = value

    @abc.abstractmethod
    def resolve(self, use_default=True):
        pass

    def first(self, use_default=True):
        pairs = self.resolve(use_default)
        try:
            return iter_first(pairs)
        except ValueError:
            raise NotFoundError(u"{0} not found".format(self.name))

    def exists(self, use_default=True):
        try:
            self.first(use_default)
            # TODO, None is not exists!
        except NotFoundError:
            return False
        return True

    @abc.abstractmethod
    def root(self):
        pass

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def __iter__(self):
        try:
            keys = self.keys()
            for key in keys:
                yield key

        except ConfigTypeError:
            collection = self.get()
            if not isinstance(collection, (list, tuple)):
                raise ConfigTypeError(
                    u"{0} must be a dictionary or a list, not {1}".format(
                        self.name, type(collection).__name__
                    )
                )

            for index in range(len(collection)):
                yield self[index]

    def __getitem__(self, key):
        return Subview(self, key, value_converter=self.value_converter)

    def __setitem__(self, key, value):
        self.set({key: value})

    def __contains__(self, key):
        return self[key].exists()

    @classmethod
    def _build_namespace_dict(cls, obj):
        output = {}

        if not isinstance(obj, dict):
            return obj

        for key in sorted(list(obj.keys())):
            value = obj[key]
            if value is None:  # Avoid unset options.
                continue

            save_to = output
            result = cls._build_namespace_dict(value)
            split = key.split(".")
            if len(split) > 1:
                key = split.pop()
                for child_key in split:
                    if child_key in save_to and isinstance(
                        save_to[child_key], dict
                    ):
                        save_to = save_to[child_key]
                    else:
                        save_to[child_key] = {}
                        save_to = save_to[child_key]

            if key in save_to:
                save_to[key].update(result)
            else:
                save_to[key] = result
        return output

    def flatten(self, redact=False):
        od = OrderedDict()
        for key, view in self.items():
            try:
                od[key] = view.flatten(redact=redact)
            except ConfigTypeError:
                od[key] = view.get()
        return od

    def set_args(self, namespace):
        self.set(self._build_namespace_dict(namespace))

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.get())

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return bool(self.get())

    def render(self, tpl: StrTemplate, additional_dict: Optional[Dict[Text, Any]] = {}):
        param = {k: v.get() for k, v in self.items()}
        param.update(additional_dict)
        return tpl.substitute(param)

    def keys(self):
        keys = []

        for dic, _ in self.resolve():
            try:
                cur_keys = dic.keys()
            except AttributeError:
                raise ConfigTypeError(
                    u"{0} must be a dict, not {1}".format(
                        self.name, type(dic).__name__
                    )
                )

            for key in cur_keys:
                if key not in keys:
                    keys.append(key)

        return keys

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def values(self):
        for key in self.keys():
            yield self[key]

    def all_contents(self):
        for collection, _ in self.resolve():
            try:
                it = iter(collection)
            except TypeError:
                raise ConfigTypeError(
                    u"{0} must be an iterable, not {1}".format(
                        self.name, type(collection).__name__
                    )
                )
            for value in it:
                yield value

    def get(self, template=None):
        return as_template(template).value(self, template, self.value_converter)

    def as_filename(self, relative_to=None):
        base_path = None
        if relative_to:
            if relative_to not in self.relatives:
                raise KeyError(
                    "relative_to varaible '%s' not set, supported: %s"
                    % (relative_to, self.relatives)
                )
            base_path = self.relatives[relative_to]
        return self.get(Filename(relative_to=base_path))

    def as_bool(self, default=False):
        return self.get() and self.as_str() in ("true", "True", "1")

    def as_choice(self, choices):
        return self.get(Choice(choices))

    def as_number(self, default=None):
        return self.get(Number(default))

    def as_str_seq(self, split=True):
        return self.get(StrSeq(split=split))

    def as_pairs(self, default_value=None):
        return self.get(Pairs(default_value=default_value))

    def as_str(self, default=None):
        return self.get(String(default))

    def as_str_expanded(self):
        return self.get(String(expand_vars=True))

    def as_sunit(self):
        return self.get(StorageUnit())


class RootView(ConfigView):
    def __init__(self, sources, value_converter=None):
        self.sources = list(sources)
        self.name = _ROOT_NAME
        super(RootView, self).__init__(value_converter=value_converter)

    def add(self, obj):
        self.sources.append(ConfigSource.of(obj))

    def set(self, value):
        self.sources.insert(0, ConfigSource.of(value))

    def resolve(self, search_default=True):
        sources = [
            source
            for source in self.sources
            if search_default or not source.default
        ]
        return ((dict(s), s) for s in sources)

    def clear(self):
        del self.sources[:]

    def root(self):
        return self


class Subview(ConfigView):
    def __init__(self, parent, key, value_converter=None):
        self.parent = parent
        self.key = key
        self.value_converter = value_converter

        if isinstance(self.parent, RootView):
            self.name = ""
        else:
            self.name = self.parent.name
            if not isinstance(self.key, int):
                self.name += "."
        if isinstance(self.key, int):
            self.name += u"#{0}".format(self.key)
        elif isinstance(self.key, bytes):
            self.name += self.key.decode("utf-8")
        elif isinstance(self.key, str):
            self.name += self.key
        else:
            self.name += repr(self.key)

    def resolve(self, use_default=True):
        for collection, source in self.parent.resolve(use_default):
            try:
                value = collection[self.key]
            except IndexError:
                continue
            except KeyError:
                continue
            except TypeError:
                raise ConfigTypeError(
                    u"{0} must be a collection, not {1}".format(
                        self.parent.name, type(collection).__name__
                    )
                )
            yield value, source

    def add(self, value):
        self.parent.add({self.key: value})

    def root(self):
        return self.parent.root()

    def set(self, value):
        self.parent.set({self.key: value})

    @property
    def relatives(self):
        return self.parent.relatives


class Loader(yaml.SafeLoader):
    def _construct_unicode(self, node):
        return self.construct_scalar(node)

    def construct_yaml_map(self, node):
        d = OrderedDict()
        yield d
        value = self.construct_mapping(node)
        d.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "except map node, found %s " % node.id,
                node.start_mark,
            )

        m = OrderedDict()
        for k_node, v_node in node.value:
            key = self.construct_object(k_node, deep=deep)
            try:
                hash(key)
            except TypeError as exec:
                raise yaml.constructor.ConstructorError(
                    context="while constructing a mapping",
                    context_mark=node.start_mark,
                    problem="found unacceptable key : %s" % exec,
                    problem_mark=k_node.start_mark,
                )

            value = self.construct_object(v_node, deep=deep)
            m[key] = value
        return m

    def check_plain(self):
        plain = super(Loader, self).check_plain()
        return plain or self.peek() == "%"


Loader.add_constructor("tag:yaml.org,2002:str", Loader._construct_unicode)
Loader.add_constructor("tag:yaml.org,2002:map", Loader.construct_yaml_map)
Loader.add_constructor("tag:yaml.org,2002:omap", Loader.construct_yaml_map)


def load(fn: Text):
    try:
        with open(fn, "rb") as fd:
            return yaml.load(fd, Loader=Loader)
    except (IOError, yaml.error.YAMLError) as exec:
        raise ConfigError(fn, exec)


class Dumper(yaml.SafeDumper):
    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        node = yaml.MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = False
        if hasattr(mapping, "items"):
            mapping = list(mapping.items())
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (
                isinstance(node_key, yaml.ScalarNode) and not node_key.style
            ):
                best_style = False
            if not (
                isinstance(
                    node_value, yaml.ScalarNode) and not node_value.style
            ):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node

    def represent_list(self, data):
        node = super(Dumper, self).represent_list(data)
        length = len(data)
        if self.default_flow_style is None and length < 4:
            node.flow_style = True
        elif self.default_flow_style is None:
            node.flow_style = False
        return node

    def represent_none(self, data):
        """Represent a None value with nothing instead of 'none'.
        """
        return self.represent_scalar("tag:yaml.org,2002:null", "")


Dumper.add_representer(OrderedDict, Dumper.represent_dict)
Dumper.add_representer(type(None), Dumper.represent_none)
Dumper.add_representer(list, Dumper.represent_list)


def restore_yaml_comments(data, default_data):
    comment_map = dict()
    default_lines = iter(default_data.splitlines())
    for line in default_lines:
        if not line:
            comment = "\n"
        elif line.startswith("#"):
            comment = "{0}\n".format(line)
        else:
            continue
        while True:
            line = next(default_lines)
            if line and not line.startswith("#"):
                break
            comment += "{0}\n".format(line)
        key = line.split(":")[0].strip()
        comment_map[key] = comment
    out_lines = iter(data.splitlines())
    out_data = ""
    for line in out_lines:
        key = line.split(":")[0].strip()
        if key in comment_map:
            out_data += comment_map[key]
        out_data += "{0}\n".format(line)
    return out_data


def _package_path(name):
    loader = pkgutil.get_loader(name)
    if loader is None or name == "__main__":
        return None

    if hasattr(loader, "get_filename"):
        filepath = loader.get_filename(name)
    else:
        __import__(name)
        filepath = sys.modules[name].__file__
    return os.path.dirname(os.path.abspath(filepath))


class Configuration(RootView):
    def __init__(self, default=None, *overrides, **kwargs):
        if "value_converter" in kwargs:
            value_converter = kwargs["value_converter"]
        else:
            value_converter = None
        super(Configuration, self).__init__([], value_converter)
        if not default:
            return

        for override in overrides:
            self.add(
                ConfigSource(load(override), filename=override, default=False)
            )

        self.add(ConfigSource(load(default), filename=default, default=True))

    def dump(self, full=True):
        if full:
            out_dict = self.flatten()
        else:
            # Exclude defaults when flattening.
            sources = [s for s in self.sources if not s.default]
            temp_root = RootView(sources)
            out_dict = temp_root.flatten()

        yaml_out = yaml.dump(
            out_dict,
            Dumper=Dumper,
            default_flow_style=None,
            indent=4,
            width=1000,
        )

        # Restore comments to the YAML text.
        default_source = None
        for source in self.sources:
            if source.default:
                default_source = source
                break
        if default_source and default_source.filename:
            with open(default_source.filename, "rb") as fp:
                default_data = fp.read()
            yaml_out = restore_yaml_comments(
                yaml_out, default_data.decode("utf-8")
            )

        return yaml_out


REQUIRED = object()


class Template(object):
    def __init__(self, default=REQUIRED):
        self.default = default

    def __call__(self, view):
        return self.value(view, self)

    def value(self, view, template=None, value_converter=None):
        if view.exists():
            value, _ = view.first()
            if value_converter is not None:
                value = value_converter(value)
            return self.convert(value, view)
        elif self.default is REQUIRED:
            raise NotFoundError(u"{0} not found".format(view.name))
        else:
            return self.default

    def convert(self, value, view):
        return value

    def fail(self, message, view, type_error=False):
        exc_class = ConfigTypeError if type_error else ConfigValueError
        raise exc_class(u"{0}: {1}".format(view.name, message))

    def __repr__(self):
        return "{0}({1})".format(
            type(self).__name__,
            "" if self.default is REQUIRED else repr(self.default),
        )


class Integer(Template):
    def convert(self, value, view):
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return int(value)
        else:
            self.fail(u"must be a number", view, True)


class Number(Template):
    def convert(self, value, view):
        if isinstance(value, (int, float)):
            return value
        else:
            self.fail(
                u"must be numeric, not {0}".format(type(value).__name__),
                view,
                True,
            )


class MappingTemplate(Template):
    def __init__(self, mapping):
        subtemplates = {}
        for key, typ in mapping.items():
            subtemplates[key] = as_template(typ)
        self.subtemplates = subtemplates

    def value(self, view, template=None, value_converter=None):
        out = AttrDict()
        for key, typ in self.subtemplates.items():
            out[key] = typ.value(
                view[key], self, value_converter=value_converter
            )
        return out

    def __repr__(self):
        return "MappingTemplate({0})".format(repr(self.subtemplates))


class Sequence(Template):
    def __init__(self, subtemplate):
        self.subtemplate = as_template(subtemplate)

    def value(self, view, template=None, value_converter=None):
        out = []
        for item in view:
            out.append(
                self.subtemplate.value(
                    item, self, value_converter=value_converter
                )
            )
        return out

    def __repr__(self):
        return "Sequence({0})".format(repr(self.subtemplate))


class String(Template):
    def __init__(self, default=REQUIRED, pattern=None, expand_vars=False):
        super(String, self).__init__(default)
        self.pattern = pattern
        self.expand_vars = expand_vars
        if pattern:
            self.regex = re.compile(pattern)

    def __repr__(self):
        args = []

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        if self.pattern is not None:
            args.append("pattern=" + repr(self.pattern))

        return "String({0})".format(", ".join(args))

    def convert(self, value, view):
        if value is None:
            return self.default
        if not isinstance(value, str):
            self.fail(u"must be a string", view, True)

        if self.pattern and not self.regex.match(value):
            self.fail(u"must match the pattern {0}".format(self.pattern), view)

        if self.expand_vars:
            return os.path.expandvars(value)
        else:
            return value


class Choice(Template):
    def __init__(self, choices, default=REQUIRED):
        super(Choice, self).__init__(default)
        self.choices = choices

    def convert(self, value, view):
        if isinstance(self.choices, type) and issubclass(
            self.choices, enum.Enum
        ):
            try:
                return self.choices(value)
            except ValueError:
                self.fail(
                    u"must be one of {0!r}, not {1!r}".format(
                        [c.value for c in self.choices], value
                    ),
                    view,
                )

        if value not in self.choices:
            self.fail(
                u"must be one of {0!r}, not {1!r}".format(
                    list(self.choices), value
                ),
                view,
            )

        if isinstance(self.choices, collections.abc.Mapping):
            return self.choices[value]
        else:
            return value

    def __repr__(self):
        return "Choice({0!r})".format(self.choices)


class StorageUnit(Template):
    def __init__(self, default=REQUIRED):
        super(StorageUnit, self).__init__(default)

    def convert(self, value, view):
        if not isinstance(value, str):
            self.fail("must be str", view, True)

        try:
            return StorageUnitModel(value)
        except ValueError as e:
            self.fail(e, view)


class OneOf(Template):
    def __init__(self, allowed, default=REQUIRED):
        super(OneOf, self).__init__(default)
        self.allowed = list(allowed)

    def __repr__(self):
        args = []

        if self.allowed is not None:
            args.append("allowed=" + repr(self.allowed))

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        return "OneOf({0})".format(", ".join(args))

    def value(self, view, template):
        self.template = template
        return super(OneOf, self).value(view, template)

    def convert(self, value, view):
        is_mapping = isinstance(self.template, MappingTemplate)

        for candidate in self.allowed:
            try:
                if is_mapping:
                    if (
                        isinstance(candidate, Filename)
                        and candidate.relative_to
                    ):
                        next_template = candidate.template_with_relatives(
                            view, self.template
                        )

                        next_template.subtemplates[view.key] = as_template(
                            candidate
                        )
                    else:
                        next_template = MappingTemplate({view.key: candidate})

                    return view.parent.get(next_template)[view.key]
                else:
                    return view.get(candidate)
            except ConfigTemplateError:
                raise
            except ConfigError:
                pass
            except ValueError as exc:
                raise ConfigTemplateError(exc)

        self.fail(
            u"must be one of {0}, not {1}".format(
                repr(self.allowed), repr(value)
            ),
            view,
        )


class StrSeq(Template):
    def __init__(self, split=True, default=REQUIRED):
        super(StrSeq, self).__init__(default)
        self.split = split

    def _convert_value(self, x, view):
        if isinstance(x, str):
            return x
        elif isinstance(x, bytes):
            return x.decode("utf-8", "ignore")
        else:
            self.fail(u"must be a list of strings", view, True)

    def convert(self, value, view):
        if isinstance(value, bytes):
            value = value.decode("utf-8", "ignore")

        if isinstance(value, str):
            if self.split:
                value = value.split()
            else:
                value = [value]
        else:
            try:
                value = list(value)
            except TypeError:
                self.fail(
                    u"must be a whitespace-separated string or a list",
                    view,
                    True,
                )
        return [self._convert_value(v, view) for v in value]


class Pairs(StrSeq):
    def __init__(self, default_value=None):
        super(Pairs, self).__init__(split=True)
        self.default_value = default_value

    def _convert_value(self, x, view):
        try:
            return (
                super(Pairs, self)._convert_value(x, view),
                self.default_value,
            )
        except ConfigTypeError:
            if isinstance(x, abc.Mapping):
                if len(x) != 1:
                    self.fail(u"must be a single-element mapping", view, True)
                k, v = iter_first(x.items())
            elif isinstance(x, abc.Sequence):
                if len(x) != 2:
                    self.fail(u"must be a two-element list", view, True)
                k, v = x
            else:
                # Is this even possible? -> Likely, if some !directive cause
                # YAML to parse this to some custom type.
                self.fail(
                    u"must be a single string, mapping, or a list" u""
                    + str(x),
                    view,
                    True,
                )
            return (
                super(Pairs, self)._convert_value(k, view),
                super(Pairs, self)._convert_value(v, view),
            )


class Filename(Template):
    def __init__(self, default=REQUIRED, relative_to=None):
        super(Filename, self).__init__(default)
        self.relative_to = relative_to

    def __repr__(self):
        args = []

        if self.default is not REQUIRED:
            args.append(repr(self.default))

        if self.relative_to is not None:
            args.append("relative_to=" + repr(self.relative_to))

        return "Filename({0})".format(", ".join(args))

    def value(self, view, template=None, value_converter=None):
        path, source = view.first()
        if not isinstance(path, str):
            self.fail(
                u"must be a filename, not {0}".format(type(path).__name__),
                view,
                True,
            )

        if urllib.parse.urlparse(path).netloc:
            return path

        pure_path = pathlib.Path(path)
        if self.relative_to and not pure_path.is_absolute():
            pure_path = os.path.join(self.relative_to, pure_path.as_posix())
        else:
            pure_path = pure_path.as_posix()
        return pure_path


class TypeTemplate(Template):
    def __init__(self, typ, default=REQUIRED):
        super(TypeTemplate, self).__init__(default)
        self.typ = typ

    def convert(self, value, view):
        if not isinstance(value, self.typ):
            self.fail(
                u"must be a {0}, not {1}".format(
                    self.typ.__name__, type(value).__name__,
                ),
                view,
                True,
            )
        return value


class AttrDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(key)


def as_template(value):
    if isinstance(value, Template):
        # If it's already a Template, pass it through.
        return value
    elif isinstance(value, collections.abc.Mapping):
        # Dictionaries work as templates.
        return MappingTemplate(value)
    elif value is int:
        return Integer()
    elif isinstance(value, int):
        return Integer(value)
    elif isinstance(value, type) and issubclass(value, str):
        return String()
    elif isinstance(value, str):
        return String(value)
    elif isinstance(value, set):
        # convert to list to avoid hash related problems
        return Choice(list(value))
    elif isinstance(value, type) and issubclass(value, enum.Enum):
        return Choice(value)
    elif isinstance(value, list):
        return OneOf(value)
    elif value is float:
        return Number()
    elif value is None:
        return Template()
    elif value is dict:
        return TypeTemplate(collections.abc.Mapping)
    elif value is list:
        return TypeTemplate(collections.abc.Sequence)
    elif isinstance(value, type):
        return TypeTemplate(value)
    else:
        raise ValueError(u"cannot convert to template: {0!r}".format(value))
