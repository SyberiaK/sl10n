# sl10n

[![PyPI release]][pypi] 
![Python supported versions] 
![License] \
![Tests] 
[![Documentation status]][docs]


sl10n is a library that takes a unique approach to dealing with localization by using statically typed translation keys.

## Features

- **Type-safe:** we use statically typed translation keys, so you don't have to worry about making a typo or using a wrong key.
- **Explicit:** you get the exact result that you expect.
- **Versatile**: you can use it in any project.
- **Self-sufficient, no other tools required.**
- **Written purely on Python.**
- **Easy to use**.
- **Small.**

## Why?

Imagine you have a `lang` folder containing all our translation files and a parser that reads these files and stores them in mapping.
```json
{
    "my_key_1": "My text",
    "my_key_2": "Wrong text"
}
```

```python
import parser  # your handwritten parser

locales = parser.parse('/lang')
locale = locales.get('en')

print(locale.get('my_key_1'))  # My text
```

You may probably think "Sounds pretty simple" and you'd be right. This approach is pretty common (e.g., Minecraft mods use it).

But it's really error-prone. You can easily make a typo or refer to a different key with similar name.

```python
print(locale.get('my_key_I'))  # my_key_I
print(locale.get('my_key_2'))  # Wrong text
```

This becomes a real trouble once you change the schema of your translation files and even IDEs won't help you.

## So?

sl10n fixes this by introducing *locale containers*.

In short, a *locale container* is a spec of your translation files that contains all possible keys.
At parsing, all your localization gets collected into locale containers, so you can access them freely.

sl10n defines a base class for your locale container (`SLocale`) and a parsing system (`SL10n`).

```python
from sl10n import SL10n, SLocale


class MyLocale(SLocale):  # your locale container, it MUST inherit from SLocale
    my_key_1: str
    my_key_2: str


l10n = SL10n(MyLocale, 'lang')  # creating a reference for system

l10n.init()  # execute parser
```

The key difference is that now you can access your translated strings as class attributes.

```python
locale: MyLocale = l10n.locale('en')  # returns default one if this language wasn't found

print(locale.my_key_1)  # My text
```

That way, your IDE can suggest what keys you can use and also tell you if you made a typo.

```python
print(locale.my_key_I)  # Unresolved attribute reference 'my_key_I for class 'MyLocale' 
```

You can still access your locale container dynamically if you want (e.g. when the key is known only at runtime).

```python
key = f()  # returned 'my_key_1'

print(locale.get(key))  # My text
```

## Other features?

- If your translation files don't follow the spec - `SL10n` will notify you and also try to fix it:
  - add all undefined keys
  - move all unexpected keys to the bottom of the file

- You can also create new translation files:

  ```python
  from sl10n import SL10n, SLocale
  
  
  class MyLocale(SLocale):
      my_key_1: str
      my_key_2: str
  
  
  l10n = SL10n(MyLocale, 'lang')
  
  l10n.create_lang_file('de')  # copy the contents of default language file ('en') to a new file
  ```

- Define what filenames should be ignored:

  ```python
  l10n = SL10n(MyLocale, 'lang', ignore_filenames=['config', 'tags'])
  ```

- Choose a different JSON parsing implementation (one of [supported](#parsing-impl)):

  ```python
  from sl10n.pimpl import JSONImpl
  import ujson
  
  l10n = SL10n(MyLocale, 'lang', parsing_impl=JSONImpl(ujson))
  ```

- Apply some modifiers to your file (todo: make a docs explaining modifiers):
  ```json
  {
      "my_key_1": "My text",
      "my_key_2": "Wrong text",
      "$redump": true  // redumps the file anyway
  }
  ```
  ```json
  {
      "my_key_1": "My text",
      "my_key_2": "<not finished>",
      "$exclude": true  // excludes the file from parsing
  }
  ```

### <a name="parsing-impl"></a>parsing_impl supports:
- `json` - builtin
- `simplejson` - loads faster, dumps slower
- `python-rapidjson` - loads slower, dumps faster
- `ujson` - loads and dumps much faster
- `orjson` - loads and dumps much faster (use `ORJSONImpl`)

### parsing_impl not supports:
- `ijson` (complicated by multiple backends and lack of `dump()`-like function)
- any non-JSON parser


[pypi]: https://pypi.org/project/sl10n/
[PyPI Release]: https://img.shields.io/pypi/v/sl10n.svg?label=pypi&color=green
[Python supported versions]: https://img.shields.io/pypi/pyversions/sl10n.svg?label=%20&logo=python&logoColor=white
[License]: https://img.shields.io/pypi/l/sl10n.svg?style=flat&label=license
[Tests]: https://github.com/SyberiaK/sl10n/actions/workflows/test.yml/badge.svg
[docs]: https://syberiak.github.io/sl10n
[Documentation status]: https://github.com/SyberiaK/sl10n/actions/workflows/docs-publish.yml/badge.svg
