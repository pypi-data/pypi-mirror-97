from pathlib import Path
from typing import Union

from tomlkit import exceptions, parse

from .base_config import BaseConfig


class TomlConfig(BaseConfig):
    def __init__(self, *, data: Union[bytes, str], path: Union[Path, str]):
        super(TomlConfig, self).__init__()
        self.is_empty_config = False
        self._parse_setting(data)
        self.add_path(path)

    def init_empty_config_content(self):
        with open(self.path, "a") as toml_file:
            toml_file.write("[tool.commitizen]")

    def set_key(self, key, value):
        """Set or update a key in the conf.

        For now only strings are supported.
        We use to update the version number.
        """
        with open(self.path, "rb") as f:
            parser = parse(f.read())

        parser["tool"]["commitizen"][key] = value
        with open(self.path, "wb") as f:
            f.write(parser.as_string().encode("utf-8"))
        return self

    def _parse_setting(self, data: Union[bytes, str]):
        """We expect to have a section in pyproject looking like

        ```
        [tool.commitizen]
        name = "cz_conventional_commits"
        ```
        """
        doc = parse(data)
        try:
            self.settings.update(doc["tool"]["commitizen"])
        except exceptions.NonExistentKey:
            self.is_empty_config = True
