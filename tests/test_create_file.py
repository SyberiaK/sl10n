from pathlib import Path

import pytest
from sl10n import SL10n
from sl10n.warnings import SL10nAlreadyInitialized, UndefinedLocale

from . import *


def test_l10n_create_file():
    path = Path(__file__).parent / 'data' / 'test_l10n_create_file'
    l10n = SL10n(Locale, path)

    is_equal(l10n.default_lang, EN)

    l10n.create_lang_file('fr')

    l10n.init()

    locale: Locale = l10n.locale(FR)
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, FR)

    # Must be a copy of default lang file (EN in this example)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")


def test_l10n_create_file_after_init():
    path = Path(__file__).parent / 'data' / 'test_l10n_create_file_after_init'
    l10n = SL10n(Locale, path).init()

    is_equal(l10n.default_lang, EN)

    with pytest.warns(SL10nAlreadyInitialized):
        l10n.create_lang_file('fr')

    with pytest.warns(UndefinedLocale):
        locale: Locale = l10n.locale(FR)

    assert locale is not None, 'Expected locale to be not None'
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
