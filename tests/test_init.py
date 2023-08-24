from pathlib import Path

import pytest

from sl10n import SL10n
from sl10n.warnings import DefaultLangFileNotFound, SL10nAlreadyInitialized

from . import *


def test_init():
    path = Path(__file__).parent / 'data' / 'test_locale_en'
    l10n = SL10n(Locale, path)

    is_equal(l10n.initialized, False)

    l10n.init()

    is_equal(l10n.initialized, True)


def test_init_default_missing():
    path = Path(__file__).parent / 'data' / 'test_locale_empty'
    l10n = SL10n(Locale, path)

    is_equal(l10n.initialized, False)

    with pytest.warns(DefaultLangFileNotFound):
        l10n.init()

    is_equal(l10n.initialized, True)


def test_warn_init_twice():
    path = Path(__file__).parent / 'data' / 'test_locale_en'
    l10n = SL10n(Locale, path).init()

    with pytest.warns(SL10nAlreadyInitialized):
        l10n.init()
