from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import TypeVar
import warnings

from .warnings import UnexpectedLocaleKey


T = TypeVar('T', bound='SLocale')


DATACLASS_PARAMS = dict(frozen=True)


@dataclass(**DATACLASS_PARAMS)
class SLocale:
    """
    This class contains some specific fields and methods to your locale containers.

    Also, you must subclass your locale container from this class to use it in ``SL10n``.
    """

    lang_code: str | None
    """
    Current locale lang code (filename). Can be overwritten only by "$lang_code" modifier.
    
    Sets to ``None`` if the container is a sample one.
    """

    def __init_subclass__(cls, *args, **kwargs):
        return dataclass(**DATACLASS_PARAMS)(cls)

    @classmethod
    def sample(cls) -> T:
        """
        Returns:
            A sample locale container with key names as values.

        ``SLocale.lang_code`` sets to None.

        Example:
            ```python
            class MyLocale(sl10n.SLocale):
                my_key_1: str
                my_key_2: str
                ...

            sample = MyLocale.sample()  # MyLocale(lang_code=None, my_key_1='my_key_1', my_key_2='my_key_2', ...)
            ```
        """

        _fields = (k.name for k in fields(cls))
        data: dict[str, str | None] = {field: field for field in _fields}
        data['lang_code'] = None
        return cls(**data)

    def to_dict(self) -> dict[str, str | None]:
        """
        Returns:
            A dict converted from a locale container.

        Example:
            ```python
            class MyLocale(sl10n.SLocale):
                my_key_1: str
                my_key_2: str
                ...

            ...

            locale = l10n.locale('en')
            locale_dict = locale.to_dict()  # {'lang_code': 'en', my_key_1: 'Text 1', my_key_2: 'Text 2', ...}
            ```
        """

        return asdict(self)

    def get(self, key: str) -> str:
        """
        Returns a string associated with the given key (if such
        a key exists, otherwise returns the key itself).

        Can be used if the key is known only at runtime.

        Parameters:
            key (str):
                Key used to get string.

        Returns:
            If such a key exists, string associated with the given key.
            Otherwise, the key itself.

        Warns:
            UnexpectedLocaleKey: When got an unexpected key.

        Example:
            ```python
            class MyLocale(sl10n.SLocale):
                my_key_1: str
                my_key_2: str
                ...

            ...

            locale = l10n.locale('en')
            my_text_1 = locale.get('my_key_1')  # 'Text 1'
            ```
        """

        try:
            return getattr(self, key)
        except AttributeError:
            warnings.warn(f'Got unexpected key "{key}", returned the key', UnexpectedLocaleKey, stacklevel=2)
            return key
