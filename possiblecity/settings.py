# -*- coding: utf-8 -*-
# Default Django settings for possiblecity

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Douglas Meehan', 'dmeehan@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "dev.db",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True    #internationalization machinery
USE_L10N = True    #format dates, numbers and calendars according to locale


#==============================================================================
# Project URLS and media settings
#==============================================================================

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

ROOT_URLCONF = 'possiblecity.urls'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")
MEDIA_URL = "/site_media/media/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")
STATIC_URL = "/site_media/static/"

ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "staticfiles.context_processors.static",

    "pinax.core.context_processors.pinax_settings",

    "pinax.apps.account.context_processors.account",
]


TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

#==============================================================================
# Middleware
#==============================================================================


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

#==============================================================================
# Fixtures
#==============================================================================

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

#==============================================================================
# Messages
#==============================================================================

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    #'django.contrib.gis',

    # third party backend apps
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "mailer",
    "django_openid",
    'haystack', # search
    'south', # database migrations
    "timezones",
    "metron", # analytics and metrics

    # third party frontend apps
    #'django_generic_flatblocks',
    #'emailconfirmation',
    #'oembed',
    #'imagekit',
    'django_markup', # required for blog
    'taggit', # required for blog, float, & lotxlot
     #'notification',

    # Third party Pinax apps
    #'pinax.templatetags',
    #'pinax.apps.account',
    #'pinax.apps.signup_codes',

    # Pinax theme
    #"pinax_theme_bootstrap",

    # backbeat apps
    'blog',
    'inlines',
    'twittools',

    # local apps
    #'about',
    #'float',
    #'lotxlot',

)

#==============================================================================
# Logging
#==============================================================================


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



#==============================================================================
# Third party app settings
#==============================================================================

# django-compressor is turned off by default due to deployment overhead for
# most users.
COMPRESS = False
COMPRESS_OUTPUT_DIR = "cache"

# django-haystack
HAYSTACK_SITECONF = 'possiblecity.search_sites'

# django-mailer
EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

# Account
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = True
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"
LOGOUT_REDIRECT_URLNAME = "home"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

#==============================================================================
# local app settings
#==============================================================================

BLOG_MARKUP_DEFAULT = 'markdown'


#==============================================================================
# local environment settings
#==============================================================================

try:
    from local_settings import *
except ImportError:
    pass