import json
from pathlib import Path

import pytest
import rapidjson
import simplejson
from sl10n import SL10n
from sl10n.pimpl import JSONImpl, ORJSONImpl
import ujson

from . import *


@pytest.mark.parametrize("module", [
    json, simplejson, rapidjson, ujson
])
def test_parsing_impl_basic(module):
    path = Path(__file__).parent / 'data' / 'test_locale_en'
    l10n = SL10n(Locale, path, parsing_impl=JSONImpl(module)).init()

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")


def test_parser_impl_orjson():
    path = Path(__file__).parent / 'data' / 'test_locale_en'
    l10n = SL10n(Locale, path, parsing_impl=ORJSONImpl()).init()

    is_equal(l10n.default_lang, EN)

    locale: Locale = l10n.locale()
    is_equal(type(locale), Locale)

    is_equal(locale.lang_code, EN)
    is_equal(locale.topic_title, "Basic 'for' loop algorithm")
    is_equal(locale.topic_text, TOPIC_TEXT_EN)
    is_equal(locale.topic_conclusion, "Now you know basic 'for' loop algorithm!")