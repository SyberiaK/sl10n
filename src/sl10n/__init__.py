"""Static localization system that reduces the headache of working with localization"""

__version__ = '0.3.0.0'

import logging

UTF8 = 'utf-8'
LOGGER = logging.getLogger('sl10n')

from .core import SL10n
from .locale import SLocale
