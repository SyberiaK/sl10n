from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, IO


class ParsingImpl(ABC):
    @property
    @abstractmethod
    def file_ext(self) -> str:
        return NotImplemented

    @abstractmethod
    def load(self, file: IO) -> Any:
        return NotImplemented

    @abstractmethod
    def dump(self, data: Any, file: IO) -> None:
        return
