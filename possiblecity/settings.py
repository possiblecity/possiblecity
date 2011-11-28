# Default Django settings for thepossiblecity.com.

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_ROOT = os.path.join(PROJECT_DIR, os.pardir)
PROJECT_URL = '/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Douglas Meehan', 'dmeehan@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False    #internationalization machinery
USE_L10N = True    #format dates, numbers and calendars according to locale


#==============================================================================
# Project URLS and media settings
#==============================================================================

ROOT_URLCONF = 'possiblecity.urls'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/', 'uploads/')
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'media/', 'static/')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

# TEMPLATE_CONTEXT_PROCESSORS += (
    # 'Custom context processors here',
# )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

#==============================================================================
# Middleware
#==============================================================================


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS = (
    # admin
    #'grappelli.dashboard',
    #'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # third party apps
    'django_generic_flatblocks',
    'django_markup',
    'haystack',
    'oembed',
    'south',
    'taggit',

    # backbeat apps
    'blog',
    'inlines',
    'twittools',

    # local apps

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

# django-markup

HAYSTACK_SITECONF = 'possiblecity.search_sites'

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