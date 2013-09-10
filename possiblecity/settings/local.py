# settings/local.py

from os import environ
from os.path import join, normpath

from base import *

#==============================================================================
# Debugging
#==============================================================================

DEBUG = True


#==============================================================================
# Email Configuration
#==============================================================================
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.webfaction.com')

EMAIL_HOST_PASSWORD = environ.get('DJANGO_EMAIL_PASSWORD', '')

EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'possiblecity')

EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

SERVER_EMAIL = 'info@possiblecity.co'

DEFAULT_FROM_EMAIL = 'info@possiblecity.co'

#==============================================================================
# Caching
#==============================================================================
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS += (
    'debug_toolbar',
)

#==============================================================================
# Toolbar Configuration
#==============================================================================

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

#==============================================================================
# Thumbnail Configuration
#==============================================================================

THUMBNAIL_DEBUG = True
