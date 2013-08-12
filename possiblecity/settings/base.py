# settings/base.py

import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from django.core.urlresolvers import reverse_lazy

#==============================================================================
# Path 
#==============================================================================

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)


#==============================================================================
# Managers 
#==============================================================================

ADMINS = (
    ('Douglas Meehan', 'dmeehan@gmail.com'),
)

MANAGERS = ADMINS

#==============================================================================
# Site 
#==============================================================================

SITE_ID = 1

# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

#==============================================================================
# Debugging
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG


#==============================================================================
# Secret Key 
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')


#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True    #internationalization machinery
USE_L10N = True    #format dates, numbers and calendars according to locale
USE_TZ = True

#==============================================================================
# Databases
#==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#==============================================================================
# Fixtures
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)


#==============================================================================
# Static assets
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

#==============================================================================
# Uploaded assets 
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

#==============================================================================
# Templates
#==============================================================================


# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'account.context_processors.account',
    'pinax_theme_bootstrap.context_processors.theme',
    'social_auth.context_processors.social_auth_by_name_backends',
    'apps.friends.context_processors.suggestions'
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs

TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)

#==============================================================================
# Middleware
#==============================================================================


# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware'
)


#==============================================================================
# Project URLS
#==============================================================================


# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'urls'


#==============================================================================
# Messages
#==============================================================================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


#==============================================================================
# Authentication
#==============================================================================

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.auth_backends.EmailAuthenticationBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend'
)

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
LOGIN_URL = reverse_lazy("account_login_signup")
LOGIN_REDIRECT_URL = reverse_lazy("home")

# Social Auth

LOGIN_ERROR_URL = "/account/social/connections/"

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = False

SOCIAL_AUTH_PIPELINE = [
    "libs.pipeline.prevent_duplicates",
    
    "social_auth.backends.pipeline.social.social_auth_user",
    "social_auth.backends.pipeline.user.get_username",
    "social_auth.backends.pipeline.user.create_user",
    "social_auth.backends.pipeline.social.associate_user",
    "social_auth.backends.pipeline.social.load_extra_data",
    "social_auth.backends.pipeline.user.update_user_details",
    
    "libs.pipeline.import_friends"
]

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", "")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", "")

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", "")
FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET", "")
FACEBOOK_EXTENDED_PERMISSIONS = [
    "email",
]

FACEBOOK_EXTRA_DATA = [
    ("first_name", "first_name"),
    ("last_name", "last_name"),
]

TWITTER_EXTRA_DATA = [
    ("name", "name"),
    ("screen_name", "screen_name"),
    ("profile_image_url", "profile_image_url"),
]


#==============================================================================
# Installed Apps
#==============================================================================

DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # gis add-ons
    #'django.contrib.gis',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'account', # local accounts
    'social_auth', # social accounts
    'djcelery', # async

    'compressor', # static file optimization
    'pagination', # pagination
    'south', # database migrations
    'taggit', # tagging
    'metron',
    
    # theme
    'pinax_theme_bootstrap',
    'django_forms_bootstrap'
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.core', # general helpers
    'apps.text', # blog
    'apps.projects', # user generated projects
    'apps.profiles', # user profiles
    'apps.friends', #user relationships
    #'apps.lotxlot',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


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
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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
# WSGI Configuration
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'


#==============================================================================
# Compression 
#==============================================================================


COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

#==============================================================================
# Search
#==============================================================================


#==============================================================================
# Notifications
#==============================================================================


#==============================================================================
# Analytics
#==============================================================================


#==============================================================================
# ASync
#==============================================================================

# Celery

BROKER_TRANSPORT = "redis"
BROKER_HOST = "localhost"
BROKER_PORT = 6379
BROKER_VHOST = "0"
BROKER_PASSWORD = ""
BROKER_POOL_LIMIT = 10

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_PASSWORD = ""
CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_LOG_LEVEL = "INFO"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_DISABLE_RATE_LIMITS = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_RESULT_EXPIRES = 7 * 24 * 60 * 60  # 7 Days
CELERYD_TASK_TIME_LIMIT = 120
CELERYD_TASK_SOFT_TIME_LIMIT = 120

#==============================================================================
# Local App Configuration
#==============================================================================

# Philadelphia

PHL_DATA = {
    'ADDRESSES': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Addresses/MapServer/0/',
    'ADDRESS_API': 'http://api.phillyaddress.com/address/',
    'BLOCK_API': 'http://api.phillyaddress.com/block/',
    'INTERSECTION_API': 'http://api.phillyaddress.com/intersection/',
    'LAND_USE': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaOIT-GIS_Boundaries/MapServer/11/',
    'PAPL': 'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/',
    'PAPL_LISTINGS': 'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/0/',
    'PAPL_ASSETS': 'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/1/',
    'PAPL_WEB':	'http://secure.phila.gov/PAPLPublicWeb/',
    'VACANCY': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/', 
    'VACANCY_APPEALS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/0/',
    'VACANCY_LICENSES': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/2/',
    'VACANCY_DEMOLITIONS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/4/',
    'VACANCY_DEMOLITION_PERMITS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/6/',
    'VACANCY_VIOLATIONS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/8/'
}
