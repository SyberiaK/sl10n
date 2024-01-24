# Locale containers

## Motivation

Applications can eventually grow bigger and start to be used worldwide.
Before that, you didn't think about your application audience and how to wide it,
which is now becoming crucial to succeed. Localization can significantly increase the reach
and impact of your application, as it becomes more accessible for people in different countries. 

So you decided to integrate it into your application. 

You ended up creating a `lang` folder containing all translations...
```json title="lang/en.json"
{
  "my_key_1": "My text",
  "my_key_2": "Wrong text"
}
```

...and a parser that reads these files and stores them in a mapping.

```python linenums="1"
import parser  # your handwritten parser

locales = parser.parse('/lang')
locale = locales.get('en')

print(locale.get('my_key_1'))  # My text
```

You can take any string you want by its string key.

You may think "Sounds pretty simple"... and you'd be right. 
This approach is pretty common and used in many applications (even Minecraft mods use it).

But it's really error-prone. You can easily make a typo or refer to a different key with a similar name.

```python
print(locale.get('my_key_I'))  # my_key_I
print(locale.get('my_key_2'))  # Wrong text
```

This becomes a real trouble once you change the schema of your translation files...

```json title="lang/en.json"
{
  "my_text": "My text",
  "wrong_text": "Wrong text"
}
```

```python
print(locale.get('my_key_1'))  # my_key_1
```

...or add new keys and forget about updating all the files.

```json title="lang/en.json"
{
  "my_text": "My text", 
  "correct_text": "Correct text",
  "wrong_text": "Wrong text"
}
```

```json title="lang/de.json"
{
  "my_text": "Mein Text",
  "wrong_text": "Falscher Text"
}
```

```python
locale = locales.get('de')

print(locale.get('correct_text'))  # correct_text
```

What we just described here is extremely similar to the difference between statically typed
and dynamically typed programming languages.

=== "Static typing (C#)"
    ```csharp linenums="1"
    using System;

    namespace Zero
    {
        class Program
        {
            string myString = "0";
            static void Main(string[] args)
            {
                Console.WriteLine(myString);
                
                if (myString >= 0) {  // raises an error at compile time
                    Console.WriteLine("What's kind of black magic is this?");
                }
            }
        }
    }
    ```

=== "Dynamic typing (Python)"
    ```python linenums="1"
    my_string = '0'
    print(my_string.lower())
    
    if my_string >= 0:  # raises an error at runtime only when got to this statement (!!!)
        print("What's kind of black magic is this?")
    ```

=== "Dynamic typing (JavaScript)"
    ```js linenums="1"
    let myString = "0";
    console.log(myString.toLowerCase())
    
    if (myString >= 0) {  // ...doesn't raise an error?!
        console.log("What's kind of black magic is this?")  // and in fact, this line also gets executed...
    }
    ```
    
    ??? info "An interesting fact about JavaScript"

        This is a valid JavaScript.
        ```js linenums="1"
        console.log("0" == -null)  // true
        ```
        I don't even know anymore...


The thing is nowadays we have smart IDEs and code editors that can check for those errors 
and highlight them even for dynamically typed languages and **even before we launched our program**.
That's why prototyping algorithms in languages like Python is much easier and faster now.

Sadly, we can't rely on IDE when it comes to checking what translation keys we are accessing 
as it would be really challenging to add this kind of functionality.

This is where the **locale containers** start to play.

## The concept of locale container

```markdown
my 300 billion dollar application localization spec:
- my_key_1
- my_key_2
```

The idea is to define a spec which determines what keys we can use in our application.
This also creates a layer between translation files and our program.

The spec also allows us to check for undefined, unfilled or odd localization keys.

It's really *that* simple.

## Defining a locale container

In `sl10n`, locale containers are defined by subclassing `sl10n.SLocale`:
```python linenums="1"
from sl10n import SLocale

class MyLocale(SLocale):
    my_key_1: str
    my_key_2: str
```

!!! note

    All locale container strings, even multiline ones, have `#!python str` type.

Then you need to reference it when defining an `sl10n.SL10n` object:
```python linenums="1"
from sl10n import SL10n, SLocale

class MyLocale(SLocale):
    my_key_1: str
    my_key_2: str
    
sl10n = SL10n(MyLocale)
```

That's it.
