"""Static localization system that reduces the headache of working with localization"""

UTF8 = 'utf-8'

from .core import SL10n
from .locale import SLocale

__all__ = ['SL10n', 'SLocale']
__version__ = '0.3.0.0'
