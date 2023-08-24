from __future__ import annotations

from dataclasses import fields
from pathlib import Path
from typing import Any, Type, TypeVar
import warnings

from . import LOGGER, UTF8
from .pimpl import ParsingImpl
from .locale import SLocale
from .modifiers import PreModifiers, PostModifiers
from .warnings import UndefinedLocaleKey, UnexpectedLocaleKey

T = TypeVar('T')


class _LocaleProcess:
    """
    Class that processes locales. Calling this returns a locale container.

    This class is not intended to be inherited.
    """

    EXCLUDE_SIGNAL = 0x01

    filepath: Path
    parsing_impl: ParsingImpl
    data: dict[str, Any]
    used_modifiers: tuple[str, ...]
    all_fields: tuple[str, ...]
    lc_fields: tuple[str, ...]
    all_dumped_fields: tuple[str, ...]

    def __new__(cls, locale_container: Type[T], filepath: Path, parsing_impl: ParsingImpl) -> T | None:
        cls.filepath = filepath
        cls.parsing_impl = parsing_impl

        with open(filepath, encoding=UTF8) as f:
            cls.data = parsing_impl.load(f)

        premodifiers, postmodifiers = cls.parse_modifiers()
        modifiers = dict(premodifiers._asdict(), **postmodifiers._asdict())
        cls.used_modifiers = tuple('$' + k for k, v in modifiers.items() if v is not None)

        signal = cls.apply_premodifiers(premodifiers)
        if signal == cls.EXCLUDE_SIGNAL:
            return

        cls.all_fields = tuple(k.name for k in fields(locale_container))
        cls.lc_fields = tuple(k.name for k in fields(locale_container) if k not in fields(SLocale))
        unexpected_keys = cls.find_unexpected_keys()

        cls.all_dumped_fields = cls.lc_fields + cls.used_modifiers + unexpected_keys

        if cls.any_undefined_key() or unexpected_keys:
            cls.redump()

        cls.apply_postmodifiers(postmodifiers)

        for key in unexpected_keys + cls.used_modifiers:
            del cls.data[key]

        # Join strings in arrays with '\n'
        for key, val in cls.data.items():
            if isinstance(val, list):
                cls.data[key] = '\n'.join(val)

        return locale_container(**cls.data)

    @classmethod
    def parse_modifiers(cls):
        premod, postmod = {}, {}
        for k, v in cls.data.items():
            if k.startswith('$'):
                k = k[1:]
                if k in PreModifiers._fields:
                    premod[k] = v
                elif k in PostModifiers._fields:
                    postmod[k] = v
        return PreModifiers(**premod), PostModifiers(**postmod)

    @classmethod
    def apply_premodifiers(cls, premodifiers: PreModifiers):
        if premodifiers.exclude:
            LOGGER.info(f'Excluding {cls.filepath.name}...')
            return cls.EXCLUDE_SIGNAL

    @classmethod
    def apply_postmodifiers(cls, postmodifiers: PostModifiers):
        if postmodifiers.redump:
            LOGGER.info(f'Redumping {cls.filepath.name}...')
            cls.redump()
        if postmodifiers.lang_code:
            LOGGER.info(f'Changing lang code of "{cls.filepath.name}" to "{postmodifiers.lang_code}"')
            cls.data['lang_code'] = postmodifiers.lang_code
        else:
            cls.data['lang_code'] = cls.filepath.stem

    @classmethod
    def redump(cls):
        with open(cls.filepath, 'w', encoding=UTF8) as f:
            cls.data = {key: cls.data[key] for key in cls.all_dumped_fields}  # fixing pairs order
            cls.parsing_impl.dump(cls.data, f)

    @classmethod
    def any_undefined_key(cls):
        found_undefined_keys = False
        for key in cls.lc_fields:
            if key not in cls.data.keys():
                warnings.warn(f'Found undefined key "{key}" in "{cls.filepath}"', UndefinedLocaleKey, stacklevel=4)
                cls.data[key] = key
                found_undefined_keys = True

        return found_undefined_keys

    @classmethod
    def find_unexpected_keys(cls):
        unexpected_keys = []

        for key in tuple(cls.data):
            if key not in cls.all_fields and key not in cls.used_modifiers:
                warnings.warn(f'Got unexpected key "{key}" in "{cls.filepath}"', UnexpectedLocaleKey, stacklevel=4)
                unexpected_keys.append(key)

        return tuple(unexpected_keys)
