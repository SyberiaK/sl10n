from __future__ import annotations

from dataclasses import fields
from pathlib import Path
from types import ModuleType
from typing import Any, Type, TypeVar
import warnings

from . import LOGGER, UTF8
from .locale import SLocale
from .modifiers import PreModifiers, PostModifiers
from .warnings import *

T = TypeVar('T')


class _LocaleProcess:
    """
    Class that processes locales. Calling this returns a locale container.

    This class is not intended to be inherited.
    """

    EXCLUDE_SIGNAL = 0x01

    file: Path
    json_impl: ModuleType
    data: dict[str, Any]
    premodifiers: PreModifiers
    postmodifiers: PostModifiers
    used_modifiers: tuple[str, ...]
    lc_fields: tuple[str, ...]
    all_fields: tuple[str, ...]
    any_undefined_keys: bool
    unexpected_keys: tuple[str, ...]
    all_dumped_fields: tuple[str, ...]
    
    def __new__(cls, locale_container: Type[T], file: Path, json_impl: ModuleType) -> T | None:
        cls.file = file
        cls.json_impl = json_impl

        with open(file, encoding=UTF8) as f:
            cls.data = cls.json_impl.load(f)

        cls.premodifiers, cls.postmodifiers = cls.parse_modifiers(cls.data)
        modifiers = dict(cls.premodifiers._asdict(), **cls.postmodifiers._asdict())
        cls.used_modifiers = tuple('$' + k for k, v in modifiers.items() if v is not None)

        signal = cls.apply_premodifiers()
        if signal == cls.EXCLUDE_SIGNAL:
            return

        cls.lc_fields = tuple(k.name for k in fields(locale_container) if k not in fields(SLocale))
        cls.all_fields = tuple(k.name for k in fields(SLocale)) + cls.lc_fields
        cls.any_undefined_keys = cls.any_undefined_key()
        cls.unexpected_keys = cls.find_unexpected_keys()

        cls.all_dumped_fields = cls.lc_fields + cls.used_modifiers + cls.unexpected_keys

        # Dump data with undefined and unexpected keys
        if cls.any_undefined_keys or cls.unexpected_keys:
            with open(file, 'w', encoding=UTF8) as f:
                cls.data = {key: cls.data[key] for key in cls.all_dumped_fields}  # fixing pairs order
                cls.json_impl.dump(cls.data, f, indent=2, ensure_ascii=False)

        cls.apply_postmodifiers()

        for key in cls.unexpected_keys + cls.used_modifiers:
            del cls.data[key]

        # Join strings in arrays with '\n'
        for key, val in cls.data.items():
            if isinstance(val, list):
                cls.data[key] = '\n'.join(val)

        cls.data['lang_code'] = file.stem
        return locale_container(**cls.data)

    @staticmethod
    def parse_modifiers(data):
        premod, postmod = {}, {}
        for k, v in data.items():
            if k.startswith('$'):
                k = k[1:]
                if k in PreModifiers._fields:
                    premod[k] = v
                elif k in PostModifiers._fields:
                    postmod[k] = v
        return PreModifiers(**premod), PostModifiers(**postmod)

    @classmethod
    def apply_premodifiers(cls):
        if cls.premodifiers.exclude:
            LOGGER.info(f'Excluding {cls.file.name}...')
            return cls.EXCLUDE_SIGNAL

    @classmethod
    def apply_postmodifiers(cls):
        if cls.postmodifiers.redump:
            LOGGER.info(f'Redumping {cls.file.name}...')
            with open(cls.file, 'w', encoding=UTF8) as f:
                data = {key: cls.data[key] for key in cls.all_dumped_fields}  # fixing pairs order
                cls.json_impl.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def any_undefined_key(cls):
        found_undefined_keys = False
        for key in cls.lc_fields:
            if key not in cls.data.keys():
                warnings.warn(f'Found undefined key "{key}" in "{cls.file}"', UndefinedLocaleKey, stacklevel=4)
                cls.data[key] = key
                found_undefined_keys = True

        return found_undefined_keys

    @classmethod
    def find_unexpected_keys(cls):
        unexpected_keys = []

        for key in tuple(cls.data):
            if key not in cls.all_fields and key not in cls.used_modifiers:
                warnings.warn(f'Got unexpected key "{key}" in "{cls.file}"', UnexpectedLocaleKey, stacklevel=4)
                unexpected_keys.append(key)

        return tuple(unexpected_keys)
