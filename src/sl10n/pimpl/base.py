from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, IO, NoReturn


class ParsingImpl(ABC):
    @abstractmethod
    def load(self, file: IO) -> Any:
        return NotImplemented

    @abstractmethod
    def dump(self, data: Any, file: IO) -> NoReturn:
        return NotImplemented
