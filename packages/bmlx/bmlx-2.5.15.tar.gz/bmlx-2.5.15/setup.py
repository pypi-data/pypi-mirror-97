from distutils import spawn
import glob
import os
import subprocess
import sys
import versioneer
import pathlib
import tempfile


from setuptools import find_packages
from setuptools import setup

from setuptools import Command
from distutils.command import build
from setuptools.command import develop
from distutils.command import install


__PROTO_DIRS__ = [
    "bmlx/proto",
]


class _GenProtoCommand(Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = "build protobuf modules"
    user_options = []

    def build_package_protos(self, package_root, strict_mode=False):
        from grpc.tools import protoc

        proto_files = []
        inclusion_root = os.path.abspath(package_root)
        for root, _, files in os.walk(inclusion_root):
            for filename in files:
                if filename.endswith(".proto"):
                    proto_files.append(
                        os.path.abspath(os.path.join(root, filename))
                    )

        with tempfile.TemporaryDirectory() as tmp_dir:

            for proto_file in proto_files:
                command = [
                    "grpc_tools.protoc",
                    "--proto_path={}".format(inclusion_root),
                    "--python_out={}".format(inclusion_root),
                    "--grpc_python_out={}".format(
                        tmp_dir
                    ),  # we don't need this byproduct.
                ] + [proto_file]
                if protoc.main(command) != 0:
                    if strict_mode:
                        raise Exception("error: {} failed".format(command))
                    else:
                        sys.stderr.write("warning: {} failed".format(command))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for d in __PROTO_DIRS__:
            self.build_package_protos(d)


class _BuildCommand(build.build):
    """build command is also invoked from bdist_wheel and install command, therefore
    this implementation covers the following commands:
    - pip install . (which invokes bdist_wheel)
    - python setup.py install (which invokes install command)
    - python setup.py bdist_wheel (which invokes bdist_wheel command)
    """

    def _should_generate_proto(self):
        return True

    sub_commands = [
        ("gen_proto", _should_generate_proto),
    ] + build.build.sub_commands


class _DevelopCommand(develop.develop):
    """This implementation covers the following commands:
        - pip install -e . (developmental install)
        - python setup.py develop (which is invoked from developmental install)
    """

    def run(self):
        self.run_command("gen_proto")
        # Run super().initialize_options. Command is an old-style class (i.e.
        # doesn't inherit object) and super() fails in python 2.
        develop.develop.run(self)


commands = versioneer.get_cmdclass().copy()
commands["gen_proto"] = _GenProtoCommand
commands["build"] = _BuildCommand
commands["develop"] = _DevelopCommand

tpls = [n.as_posix() for n in pathlib.Path().rglob("*.yml")]

# Get various package dependencies list.
with open("bmlx/dependencies.py") as fp:
    globals_dict = {}
    exec(fp.read(), globals_dict)  # pylint: disable=exec-used
_make_required_install_packages = globals_dict["make_required_install_packages"]
_make_required_test_packages = globals_dict["make_required_test_packages"]
_make_extra_packages_docker_image = globals_dict[
    "make_extra_packages_docker_image"
]
_make_all_dependency_packages = globals_dict["make_all_dependency_packages"]


# Get the long description from the README file.
with open("README.md") as fp:
    _LONG_DESCRIPTION = fp.read()


setup(
    name="bmlx",
    version=versioneer.get_version(),
    author="",
    author_email="",
    license="Apache 2.0",
    cmdclass=commands,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    namespace_packages=[],
    install_requires=_make_required_install_packages(),
    extras_require={
        "docker-image": _make_extra_packages_docker_image(),
        "all": _make_all_dependency_packages(),
    },
    setup_requires=["grpcio-tools>=1.14.0", "pytest-runner",],
    tests_require=_make_required_test_packages(),
    python_requires=">=3.6.*",
    packages=find_packages(),
    data_files=[("", tpls),],
    include_package_data=True,
    description="BMLX is vairiant of tfx for internal use for BIGO",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="bigo tfx",
    url="https://git.sysop.bigo.sg/mlplat/bmlx",
    download_url="https://git.sysop.bigo.sg/mlplat/bmlx",
    requires=[],
    dependency_links=[],
    # Below console_scripts, each line identifies one console script. The first
    # part before the equals sign (=) which is 'bmlx', is the name of the script
    # that should be generated, the second part is the import path followed by a
    # colon (:) with the Click command group. After installation, the user can
    # invoke the CLI using "bmlx <command_group> <sub_command> <flags>"
    entry_points="""
        [console_scripts]
        bmlx=bmlx.cli.ui.main:main
        bmlx_rt=bmlx.cli.runtime.main:main
    """,
)
