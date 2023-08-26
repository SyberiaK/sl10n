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


class _LocaleProcessor:
    """
    Class that processes locales. Calling this returns a locale container.

    This class is not intended to be inherited.
    """

    EXCLUDE_SIGNAL = 0x01

    filepath: Path
    parsing_impl: ParsingImpl
    data: dict[str, Any]
    lc_fields: list[str]
    all_dumped_fields: list[str]
    
    def __init__(self, locale_container: Type[T], parsing_impl: ParsingImpl):
        self.locale_container = locale_container
        self.parsing_impl = parsing_impl

        self.all_fields = [k.name for k in fields(locale_container)]
        self.lc_fields = [k.name for k in fields(locale_container) if k not in fields(SLocale)]
        
    def process(self, filepath: Path) -> T | None:
        self.filepath = filepath

        with open(filepath, encoding=UTF8) as f:
            self.data = self.parsing_impl.load(f)

        premodifiers, postmodifiers = self.parse_modifiers()
        modifiers = dict(premodifiers._asdict(), **postmodifiers._asdict())
        used_modifiers = ['$' + k for k, v in modifiers.items() if v is not None]

        signal = self.apply_premodifiers(premodifiers)
        if signal == self.EXCLUDE_SIGNAL:
            return

        unexpected_keys = self.find_unexpected_keys(self.all_fields + used_modifiers)
        
        self.all_dumped_fields = self.lc_fields + used_modifiers + unexpected_keys

        if self.any_undefined_key() or unexpected_keys:
            self.redump()

        self.apply_postmodifiers(postmodifiers)

        for key in used_modifiers + unexpected_keys:
            del self.data[key]

        # Join strings in arrays with '\n'
        for key, val in self.data.items():
            if isinstance(val, list):
                self.data[key] = '\n'.join(val)

        return self.locale_container(**self.data)

    def parse_modifiers(self):
        premod, postmod = {}, {}
        for k, v in self.data.items():
            if k.startswith('$'):
                k = k[1:]
                if k in PreModifiers._fields:
                    premod[k] = v
                elif k in PostModifiers._fields:
                    postmod[k] = v
        return PreModifiers(**premod), PostModifiers(**postmod)

    def apply_premodifiers(self, premodifiers: PreModifiers):
        if premodifiers.exclude:
            LOGGER.info(f'Excluding {self.filepath.name}...')
            return self.EXCLUDE_SIGNAL

    def apply_postmodifiers(self, postmodifiers: PostModifiers):
        if postmodifiers.redump:
            LOGGER.info(f'Redumping {self.filepath.name}...')
            self.redump()
        if postmodifiers.lang_code:
            LOGGER.info(f'Changing lang code of "{self.filepath.name}" to "{postmodifiers.lang_code}"')
            self.data['lang_code'] = postmodifiers.lang_code
        else:
            self.data['lang_code'] = self.filepath.stem

    def redump(self):
        with open(self.filepath, 'w', encoding=UTF8) as f:
            self.data = {key: self.data[key] for key in self.all_dumped_fields}  # fixing pairs order
            self.parsing_impl.dump(self.data, f)

    def any_undefined_key(self):
        undefined_keys = set(self.lc_fields) - set(self.data)
        for key in undefined_keys:
            warnings.warn(f'Found undefined key "{key}" in "{self.filepath}"', UndefinedLocaleKey, stacklevel=4)
            self.data[key] = key

        return bool(undefined_keys)

    def find_unexpected_keys(self, possible_fields):
        unexpected_keys = set(self.data) - set(possible_fields)

        for key in unexpected_keys:
            warnings.warn(f'Got unexpected key "{key}" in "{self.filepath}"', UnexpectedLocaleKey, stacklevel=4)

        return list(unexpected_keys)
