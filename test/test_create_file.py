from pathlib import Path

import pytest
from sl10n import SL10n
from sl10n.warnings import SL10nAlreadyInitialized, UnexpectedLocale

from . import *


def test_l10n_create_file():
    path = Path(__file__).parent / 'data' / 'test_l10n_create_file'
    l10n = SL10n(Locale, path)

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    l10n.create_lang_file('fr')

    l10n.init()

    locale: Locale = l10n.locale(FR)

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == FR, f"{locale.lang_code=}, expected {FR!r}"

    # Must be a copy of default lang file (EN in this example)
    assert locale.topic_title == "Basic 'for' loop algorithm", \
        f"{locale.topic_title=}, expected \"Basic 'for' loop algorithm\""
    assert locale.topic_text == TOPIC_TEXT_EN, \
        f"{locale.topic_text=}, expected '{TOPIC_TEXT_EN!r}'"
    assert locale.topic_conclusion == "Now you know basic 'for' loop algorithm!", \
        f"{locale.topic_conclusion=}, expected \"Now you know basic 'for' loop algorithm!\""


def test_l10n_create_file_after_init():
    path = Path(__file__).parent / 'data' / 'test_l10n_create_file_after_init'
    l10n = SL10n(Locale, path).init()

    assert l10n.default_lang == EN, f"{l10n.default_lang=}, expected {EN!r}"

    with pytest.warns(SL10nAlreadyInitialized):
        l10n.create_lang_file('fr')

    with pytest.warns(UnexpectedLocale):
        locale: Locale = l10n.locale(FR)

    assert locale is not None, 'Expected locale to be not None'
    assert type(locale) == Locale, f'{type(locale)=}, expected {Locale.__name__}'

    assert locale.lang_code == EN, f"{locale.lang_code=}, expected {EN!r}"
