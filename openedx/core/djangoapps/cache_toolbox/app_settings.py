"""
Settings for cache_toolbox.
"""

from __future__ import absolute_import

from django.conf import settings

# Default cache timeout
CACHE_TOOLBOX_DEFAULT_TIMEOUT = getattr(
    settings,
    'CACHE_TOOLBOX_DEFAULT_TIMEOUT',
    60 * 60 * 24 * 3,
)
