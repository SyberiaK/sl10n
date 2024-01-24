from __future__ import annotations

import json
from types import ModuleType
from typing import Any, IO
import warnings

from .base import ParsingImpl


__all__ = ('JSONImpl', 'ORJSONImpl')


class JSONImpl(ParsingImpl):
    """
    Interface for basic JSON parsers implementations (which follow builtin `json` interface).

    Modules confirmed as supported: ``json``, ``simplejson``, ``ujson``, ``rapidjson``
    """

    file_ext = 'json'
    """Accepts ".json" files."""

    def __init__(self, module: ModuleType = json, *args: Any, **kwargs: Any):
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
        warnings.warn('According to our benchmarks, "orjson" makes no significant load/dump speeds difference '
                      'for our use case.\n'
                      'Use sl10n.pimpl.JSONImpl() with one of the supported packages instead (e.g. built-in "json").',
                      DeprecationWarning, stacklevel=2)

        import orjson

        super().__init__(orjson, *args, **kwargs)

    def load(self, file: IO, *args, **kwargs) -> Any:
        return self.module.loads(file.read())

    def dump(self, data: Any, file: IO) -> None:
        data = self.module.dumps(data, file, *self.args, **self.kwargs)
        file.write(data)
