# Quick Start

## Installation

=== "Stable release"

    ```python
    pip install -U sl10n    
    ```

=== "Development version"

    ```python
    pip install -U "sl10n @ git+https://github.com/SyberiaK/sl10n@main" 
    ```
    !!! warning

        This version may have a lot of bugs. Please don't use it in production code.

## Import the library

To start working with sl10n, we need to import the main parts of the library.

```python linenums="1"
from src.sl10n import SL10n, SLocale
```

## Define a locale container

Locale container is an important part of sl10n functionality.
Create a SLocale subclass and define all translation keys you will have.

```python linenums="1"
class MyLocale(SLocale):
    greetings_text: str
    main_menu_title: str
    success_text: str
    error_text: str
```

!!! note

    All locale container strings, even multiline ones, have `#!python str` type.

## Initialize the SL10n

To reference the SL10n system, create an SL10n object.

```python linenums="1"
sl10n = Sl10n(MyLocale)
```

You can also define a path where your translation files are stored, what language is default,
what filenames should be ignored and what JSON parsing implementations to use:

```python linenums="1"
from pathlib import Path
import ujson  # not a stdlib

sl10n = sl10n.Sl10n(MyLocale, Path.cwd() / 'data',
                    default_lang='de',
                    ignore_filenames=['tags', 'config'],
                    json_impl=ujson)
```

Note that it only creates a *reference* to your localization system.
To load all locale files and pack their content into locale containers,
call `SL10n.init()` method:

```python linenums="1"
sl10n.init()
```

!!! tip

    `SL10n.init()` returns a reference to your SL10n object,
    so you can use this oneline to initialize immediately:

    ```python linenums="1"
    sl10n = sl10n.Sl10n(MyLocale).init()
    ```

## Put your strings into translation files

At first init, SL10n will create a default translation file 
([working_dir]/lang/en.json by default). It will look like this: 

```json
{
  "greetings_text": "greetings_text",
  "main_menu_title": "main_menu_title",
  "success_text": "success_text",
  "error_text": "error_text"
}
```

Put in your actual text.

```json
{
  "greetings_text": "Hello World!",
  "main_menu_title": "Main menu",
  "success_text": [
    "Success!",
    "Now you can go back."
  ],
  "error_text": [
    "Error!",
    "Please try again."
  ]
}
```

Later on, you can use modifiers in these files.

```json
{
  "greetings_text": "Hello World!",
  "main_menu_title": "Main menu",
  "success_text": [
    "Success!",
    "Now you can go back."
  ],
  "error_text": [
    "Error!",
    "Please try again."
  ], 
  "redump": true  // redumps the file anyway
}
```

You can also create new lang files:
```python linenums="1"
sl10n = SL10n(MyLocale)
sl10n.create_lang_file('de')
```

!!! tip

    You can pass in `override` argument to override existing file.

    ```python linenums="1"
    sl10n.create_lang_file('fr', override=True)
    ```

!!! warning

    You can create lang files **only before** SL10n init.

    ```python linenums="1"
    sl10n = SL10n(MyLocale).init()
    sl10n.create_lang_file('de')  # file not created, SL10nAlreadyInitialized warning
    ```

    This is important to ensure that all translation files were initialized.

## Get needed locale

After initializing the SL10n, you can access your locale by using `SL10n.locale(lang)`.

```python linenums="1"
# Type hint to ensure highlighting unknown attributes
locale: MyLocale = l10n.locale()

print(locale.greetings_text)  # Hello World!
```

You can access locale strings just like object attributes. 
If you do need to use string key:

```python linenums="1"
# Type hint to ensure highlighting unknown attributes
locale: MyLocale = l10n.locale('de')
key = f()  # 'greetings_text'

print(locale.get(key))  # Hallo Welt!
```

!!! warning

    If you pass an undefined key to locale.get(key) - it will return the key itself.

    ```python linenums="1"
    print(locale.get('unknown_key'))  # unknown_key
    ```

## Set up locale lookups

You can define this function for fast locale lookups:

```python linenums="1"
_l10n = SL10n(MyLocale)  # private implementation detail, don't access it directly


def locale(lang: str = None) -> MyLocale:
    if not _l10n.initialized:
        _l10n.init()  # init at first time
    return _l10n.locale(lang)
```

## Basic template

To summarize it up, here's the basic template for SL10n integration you can use as a starting point:

```python linenums="1"
from src.sl10n import SL10n, SLocale


class MyLocale(SLocale):
    greetings_text: str
    main_menu_title: str
    success_text: str
    error_text: str


_l10n = SL10n(MyLocale)


def locale(lang: str = None) -> MyLocale:
    if not _l10n.initialized:
        _l10n.init()
    return _l10n.locale(lang)


def main():
    loc = locale()  # returns default locale ('en' here)
    print(loc.greetings_text)  # Hello World!


if __name__ == "__main__":
    main()
```

If you want to know more details about each part of SL10n - check other articles.