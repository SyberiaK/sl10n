from pathlib import Path

import simplejson
from sl10n import SL10n
import ujson

from . import *


def test_l10n_init_simplejson():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path, json_impl=simplejson).init()

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")


def test_l10n_init_ujson():
    path = Path(__file__).parent / 'data' / 'test_l10n_init_default_en'
    l10n = SL10n(Locale, path, json_impl=ujson).init()

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")
