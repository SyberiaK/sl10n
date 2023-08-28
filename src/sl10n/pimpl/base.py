from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, IO


class ParsingImpl(ABC):
    """Interface for file parsing implementations."""

    @property
    @abstractmethod
    def file_ext(self) -> str:
        return NotImplemented

    @abstractmethod
    def load(self, file: IO) -> Any:
        raise NotImplementedError

    @abstractmethod
    def dump(self, data: Any, file: IO) -> None:
        raise NotImplementedError
