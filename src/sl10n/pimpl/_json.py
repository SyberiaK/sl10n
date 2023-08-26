from __future__ import annotations

import json
from types import ModuleType
from typing import Any, IO

from .base import ParsingImpl


__all__ = ('JSONImpl', 'ORJSONImpl')


class JSONImpl(ParsingImpl):
    """
    Interface for basic JSON parsers implementations (which follow builtin `json` interface).

    Supported modules: ``json``, ``simplejson``, ``ujson``, ``rapidjson``
    """

    file_ext = 'json'
    """"""

    def __init__(self, module: ModuleType = json, *args, **kwargs):
        self.module = module
        self.args = args
        self.kwargs = kwargs

    def load(self, file: IO) -> Any:
        return self.module.load(file)

    def dump(self, data: Any, file: IO) -> None:
        self.module.dump(data, file, *self.args, **self.kwargs)


class ORJSONImpl(JSONImpl):
    """
    Interface for ``orjson`` module.

    Please ensure that you have this module installed.
    """

    def __init__(self, *args, **kwargs):
        import orjson

        super().__init__(orjson, *args, **kwargs)

    def load(self, file: IO, *args, **kwargs) -> Any:
        return self.module.loads(file.read())

    def dump(self, data: Any, file: IO) -> None:
        data = self.module.dumps(data, file, *self.args, **self.kwargs)
        file.write(data)
