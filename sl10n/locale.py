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

    Also, you must subclass your locale container from this class in order to use in ``SL10n``.

    All locale containers have one reserved field - `lang_code`:
    ```python
    locale = l10n.locale('en')
    my_lang = locale.lang_code  # 'en'
    ```

    This field always equals to current locale lang (filename) and cannot be overwritten even from the file.
    """

    lang_code: str

    def __init_subclass__(cls, *args, **kwargs):
        # noinspection PyArgumentList
        return dataclass(cls, **DATACLASS_PARAMS)

    @classmethod
    def sample(cls) -> T:
        """
        Returns a sample locale container with key names as values.

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
        data = {field: field for field in _fields}
        data['lang_code'] = None
        return cls(**data)

    def to_dict(self) -> dict[str, str]:
        """
        Returns a dict converted from a locale container.

        Example:
            ```python
            class MyLocale(sl10n.SLocale):
                my_key_1: str
                my_key_2: str
                ...

            locale = l10n.locale('en')
            locale_dict = locale.to_dict()  # {'lang_code': 'en', my_key_1: 'Text 1', my_key_2: 'Text 2', ...}
            ```
        """

        return asdict(self)

    def get(self, key: str) -> str:
        """
        Returns a string associated with the given key (if such
        key exists, otherwise returns the key itself).

        Can be used if the key is known only at runtime.

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

        Parameters:
            key (str):
                Key used to get string.
        """

        try:
            return getattr(self, key)  # todo: write some tests for it
        except AttributeError:
            warnings.warn(f'Got unexpected key "{key}", returned the key', UnexpectedLocaleKey, stacklevel=2)
            return key
