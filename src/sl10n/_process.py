"""
HEY, STOP RIGHT THERE!

Be aware that this code is not intended to be used outside the module.
Any implementation detail can be changed at any time without warning.
If you need to manipulate it in any way, you're absolutely screwed.
"""

from __future__ import annotations

from dataclasses import fields
import logging
from pathlib import Path
from typing import Type, TypeVar
import warnings

from . import UTF8
from .pimpl import ParsingImpl
from .locale import SLocale
from .modifiers import PreModifiers, PostModifiers
from .warnings import UndefinedLocaleKey, UnexpectedLocaleKey, UnfilledLocaleKey, UnknownModifier

T = TypeVar('T')
logger = logging.getLogger('sl10n')


class _LocaleProcessor:
    EXCLUDE_SIGNAL = 0x01

    filepath: Path
    data: dict
    all_dumped_fields: list[str]
    
    def __init__(self, locale_container: Type[T], parsing_impl: ParsingImpl, is_strict: bool, warn_unfilled_keys: bool):
        self.locale_container = locale_container
        self.parsing_impl = parsing_impl
        self.is_strict = is_strict
        self.warn_unfilled_keys = warn_unfilled_keys

        self.all_fields = [k.name for k in fields(locale_container)]
        self.lc_fields = {k.name: k.type for k in fields(locale_container) if k not in fields(SLocale)}
        
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
        undefined_keys = self.find_undefined_keys()
        if self.warn_unfilled_keys:
            self.check_unfilled_keys()

        self.all_dumped_fields = list(self.lc_fields.keys()) + used_modifiers + unexpected_keys

        for key in undefined_keys:
            self.data[key] = key

        if undefined_keys or unexpected_keys:
            self.redump()

        self.apply_postmodifiers(postmodifiers)

        for key in used_modifiers + unexpected_keys:
            del self.data[key]

        # Join strings in arrays with '\n'
        for key, val in self.data.items():
            if isinstance(val, list):
                val = '\n'.join(val)
                self.data[key] = val

            # _type = self.lc_fields.get(key)
            # if _type is None:
            #     continue
            #
            # if not isinstance(val, _type):
            #     warnings.warn(f'Found "{key}" value having wrong type'
            #                   f' (expected: {_type.__name__}, actual: {type(val).__name__}) in "{self.filepath}"',
            #                   UserWarning, stacklevel=4)

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
            logger.debug(f'Excluding {self.filepath.name}...')
            return self.EXCLUDE_SIGNAL

    def apply_postmodifiers(self, postmodifiers: PostModifiers):
        if postmodifiers.redump:
            logger.debug(f'Redumping {self.filepath.name}...')
            self.redump()
        if postmodifiers.lang_code:
            logger.debug(f'Changing lang code of "{self.filepath.name}" to "{postmodifiers.lang_code}"')
            self.data['lang_code'] = postmodifiers.lang_code
        else:
            self.data['lang_code'] = self.filepath.stem

    def redump(self):
        with open(self.filepath, 'w', encoding=UTF8) as f:
            self.data = {key: self.data[key] for key in self.all_dumped_fields}  # fixing pairs order
            self.parsing_impl.dump(self.data, f)

    def find_undefined_keys(self):
        undefined_keys = set(self.lc_fields.keys()) - set(self.data)

        for key in undefined_keys:
            warnings.warn(f'Found undefined key "{key}" in "{self.filepath}"', UndefinedLocaleKey, stacklevel=4)

        return list(undefined_keys)

    def find_unexpected_keys(self, possible_fields):
        unexpected_keys = set(self.data) - set(possible_fields)

        for key in unexpected_keys:

            if key.startswith('$'):
                warnings.warn(f'Found unknown modifier "{key}" in "{self.filepath}"', UnknownModifier, stacklevel=4)
            else:
                warnings.warn(f'Found unexpected key "{key}" in "{self.filepath}"', UnexpectedLocaleKey, stacklevel=4)

        return list(unexpected_keys)

    def check_unfilled_keys(self):
        unfilled_keys = set(k for k, v in self.data.items() if k == v or v == '')

        for key in unfilled_keys:
            warnings.warn(f'Got unfilled key "{key}" in "{self.filepath}"', UnfilledLocaleKey, stacklevel=4)
