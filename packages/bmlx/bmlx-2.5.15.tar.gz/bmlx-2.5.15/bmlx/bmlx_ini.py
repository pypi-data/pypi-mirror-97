import configparser
import pathlib


DEFAULT_INI_DIR = ".bmlx"
DEFAULT_CONFIG_NAME = "config"


class BmlxINI:
    __slots__ = ["parser", "ini_file"]

    def __init__(self, env="prod"):
        expected_dir = pathlib.Path(pathlib.Path.home(), DEFAULT_INI_DIR)
        if expected_dir.exists() and not expected_dir.is_dir():
            raise RuntimeError(
                "bmlx ini dir : %s exists, but not a directory"
                % expected_dir.as_posix()
            )
        expected_dir.mkdir(exist_ok=True)

        expected_ini = pathlib.Path(
            expected_dir, f"{DEFAULT_CONFIG_NAME}.{env}"
        )
        if expected_ini.exists() and not expected_ini.is_file():
            raise RuntimeError(
                "bmlx ini file: %s exists, but not a file"
                % expected_ini.as_posix()
            )

        self.ini_file = expected_ini
        self.parser = configparser.ConfigParser()
        try:
            self.parser.read_file(open(self.ini_file, "r"))
        except FileNotFoundError:
            pass

        if not self.parser.has_section("login"):
            self.parser.add_section("login")

    def flush(self):
        self.parser.write(open(self.ini_file, "w"))

    @property
    def token(self):

        return self.parser["login"].get("token", "")

    @token.setter
    def token(self, token):
        self.parser["login"]["token"] = token

    @property
    def user(self):
        return self.parser["login"].get("user", "")

    @user.setter
    def user(self, user):
        self.parser["login"]["user"] = user
