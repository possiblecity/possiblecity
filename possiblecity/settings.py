# -*- coding: utf-8 -*-
# Default Django settings for possiblecity

import os.path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


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
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#==============================================================================
# Project URLS and media settings
#==============================================================================


ROOT_URLCONF = 'possiblecity.urls'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media", "uploads")
MEDIA_URL = "/media/uploads/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "media", "static")
STATIC_URL = "/media/static/"

STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
]

TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    ]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "pinax_utils.context_processors.settings",
    "account.context_processors.account",
    'social_auth.context_processors.social_auth_by_name_backends',
]

#==============================================================================
# Middleware
#==============================================================================


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
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


# Account
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True


#ABSOLUTE_URL_OVERRIDES = {
#    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
#    }

#AUTH_PROFILE_MODULE = "profiles.Profile"

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"
LOGOUT_REDIRECT_URLNAME = "home"

AUTHENTICATION_BACKENDS = (
    "social_auth.backends.twitter.TwitterBackend",
    "social_auth.backends.facebook.FacebookBackend",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_COMPLETE_URL_NAME  = "socialauth_complete"
SOCIAL_AUTH_ASSOCIATE_URL_NAME = "socialauth_associate_complete"



#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS = (
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #"django.contrib.gis",

    # theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",

    # third party apps
    "account",
    "timezones",
    "metron",
    "social_auth", # registration via social networks

    #"haystack", # search
    #"south", # database migrations
    #"oembed",
    #"imagekit",
    #"django_markup", # required for blog
    #"taggit", # required for blog, float, & lotxlot


    # backbeat apps
    #'inlines',
    #'twittools',
    #'images',
    #'text',

    # local apps
    "possiblecity.auth_utils",
    #'blog',
    #'about',
    #'profiles',
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
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
            },
        }
}


#==============================================================================
# Email
#==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
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