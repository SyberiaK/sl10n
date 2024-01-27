"""
HEY, STOP RIGHT THERE!

Be aware that this code is not intended to be used outside the module.
Any implementation detail can be changed at any time without warning.
If you need to manipulate it in any way, you're absolutely screwed.
"""

from functools import wraps
import warnings

from .exceptions import SL10nStrictException


def strict_wrapper(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not self.is_strict:
            return func(self, *args, **kwargs)

        with warnings.catch_warnings(record=True) as warnings_list:
            # warnings.simplefilter('always')
            result = func(self, *args, **kwargs)

        if warnings_list:
            raise SL10nStrictException(warnings_list)

        return result

    return inner
