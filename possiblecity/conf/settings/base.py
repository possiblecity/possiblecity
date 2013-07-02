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

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "possiblecity.wsgi.application"

#==============================================================================
# Debugging
#==============================================================================


TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

#==============================================================================
# Databases
#==============================================================================


#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False    #internationalization machinery
USE_L10N = True    #format dates, numbers and calendars according to locale
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
    "compressor.finders.CompressorFinder",
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
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
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
    "pagination.middleware.PaginationMiddleware"
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
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
#ACCOUNT_EMAIL_REQUIRED = False
#ACCOUNT_EMAIL_VERIFICATION ="mandatory"

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
    "django.contrib.humanize",
    #"django.contrib.gis",

    # third party apps 
    "allauth", #authentication
    "allauth.account", #authentication
    "allauth.socialaccount", #authentication
    "allauth.socialaccount.providers.facebook", #authentication
    "allauth.socialaccount.providers.twitter", #authentication
    "south", # database migrations
    "compressor", # static file optimization
    "pagination", # pagination
    "easy_thumbnails", # image manipulation
    "redactor", # wysiwyg editing
    "taggit", # tagging


    # local apps
    "possiblecity.core",
    "possiblecity.text",
    "possiblecity.projects",
    "possiblecity.profiles",
    #"possiblecity.lotxlot",
    #"possiblecity.philadelphia",
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

#==============================================================================
# Search
#==============================================================================



#==============================================================================
# Notifications
#==============================================================================


#==============================================================================
# Analytics
#==============================================================================

METRON_SETTINGS = {
    "google": {
        "1": "UA-28417563-1", # production
    }
}

#==============================================================================
# Assets
#==============================================================================


COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

#==============================================================================
# Other 3rd Party Apps
#==============================================================================



#==============================================================================
# Local Apps
#==============================================================================

# Philadelphia

PHL_DATA = {
    "ADDRESSES": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Addresses/MapServer/0/",
    "ADDRESS_API": "http://api.phillyaddress.com/address/",
    "BLOCK_API": "http://api.phillyaddress.com/block/",
    "INTERSECTION_API": "http://api.phillyaddress.com/intersection/",
    "LAND_USE": "http://gis.phila.gov/ArcGIS/rest/services/PhilaOIT-GIS_Boundaries/MapServer/11/",
    "PAPL": "http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/",
    "PAPL_LISTINGS": "http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/",
    "PAPL_ASSETS": "http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/1/",
    "PAPL_WEB":	"http://secure.phila.gov/PAPLPublicWeb/",
    "VACANCY": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/", 
    "VACANCY_APPEALS": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/0/",
    "VACANCY_LICENSES": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/2/",
    "VACANCY_DEMOLITIONS": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/4/",
    "VACANCY_DEMOLITION_PERMITS": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/6/",
    "VACANCY_VIOLATIONS": "http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/8/"
}


#==============================================================================
# local environment settings
#==============================================================================

try:
    from local_settings import *
except ImportError:
    pass
