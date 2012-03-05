# -*- coding: utf-8 -*-
# Default Django settings for possiblecity

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Douglas Meehan', 'dmeehan@gmail.com'),
    )

MANAGERS = ADMINS

SITE_ID = 1

#==============================================================================
# Debugging
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    }

INTERNAL_IPS = [
    "127.0.0.1",
]

#==============================================================================
# Databases
#==============================================================================

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

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media", "uploads")
MEDIA_URL = "/media/uploads"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "media", "static")
STATIC_URL = "/media/static/"

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

# django-compressor is turned off by default due to deployment overhead for
# most users.
COMPRESS = False
COMPRESS_OUTPUT_DIR = "cache"

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

    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "social_auth.context_processors.social_auth_by_type_backends",
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
    "pagination.middleware.PaginationMiddleware",
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
# Authentication
#==============================================================================

AUTHENTICATION_BACKENDS = (
    "social_auth.backends.twitter.TwitterBackend",
    "social_auth.backends.facebook.FacebookBackend",
    "social_auth.backends.google.GoogleOAuthBackend",
    "social_auth.backends.google.GoogleOAuth2Backend",
    "social_auth.backends.google.GoogleBackend",
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.OpenIDBackend',
    #'django.contrib.auth.backends.ModelBackend',
    'pinax.apps.account.auth_backends.AuthenticationBackend',
    )

# django-social-auth
SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'twitter', 'google-oauth2')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/about/what_next'
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
# SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

# Account
ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
    }

AUTH_PROFILE_MODULE = "profiles.Profile"

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"
LOGOUT_REDIRECT_URLNAME = "home"


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

    # third party apps
    'staticfiles',
    'compressor',
    'debug_toolbar',
    'mailer',
    'django_openid',
    'haystack', # search
    'south', # database migrations
    'timezones',
    'metron', # analytics and metrics
    'social_auth', # registration via social networks
    'django_generic_flatblocks',
    'emailconfirmation',
    'announcements',
    'pagination',
    'idios',
    'oembed',
    'imagekit',
    'django_markup', # required for blog
    'taggit', # required for blog, float, & lotxlot
    'notification',

    # Third party Pinax apps
    'pinax.templatetags',
    'pinax.apps.account',
    'pinax.apps.signup_codes',

    # Pinax theme
    'pinax_theme_bootstrap',

    # backbeat apps
    'inlines',
    'twittools',
    'images',
    'text',

    # local apps
    'blog',
    'about',
    'profiles',
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
# Email
#==============================================================================

# django-mailer
EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

#==============================================================================
# Search
#==============================================================================

# django-haystack
HAYSTACK_SITECONF = 'possiblecity.search_sites'


#==============================================================================
# Notifications
#==============================================================================

NOTIFICATION_LANGUAGE_MODULE = "account.Account"

#==============================================================================
# Analytics
#==============================================================================

METRON_SETTINGS = {
    "google": {
        "1": "UA-28417563-1", # production
    }
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