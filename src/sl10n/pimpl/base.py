from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, IO


class ParsingImpl(ABC):
    """
    Interface for file parsing implementations.

    You can inherit from it and define your own parsing implementation for SL10n.
    """

    @property
    @abstractmethod
    def file_ext(self) -> str:
        """
        Returns a string that represents what file extension the parsing implementation works with.

        Example:
            ```python
            class JSONImpl(ParsingImpl):
                file_ext = 'json'
            ```
        """

        return NotImplemented

    @abstractmethod
    def load(self, file: IO) -> Any:
        """
        Loads and returns data from a passed IO object (mostly file).

        Example:
            ```python
            import json

            class JSONImpl(ParsingImpl):
                def load(self, file: IO) -> Any:
                    return json.load(file)
            ```
        """

        raise NotImplementedError

    @abstractmethod
    def dump(self, data: Any, file: IO) -> None:
        """
        Saves data into a passed IO object (mostly file).

        Example:
            ```python
            import json

            class JSONImpl(ParsingImpl):
                def dump(self, data: Any, file: IO) -> None:
                    json.dump(data, file)
            ```
        """

        raise NotImplementedError
