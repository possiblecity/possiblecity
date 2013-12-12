# settings/base.py

import os
from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from djcelery import setup_loader

from django.core.urlresolvers import reverse_lazy

#==============================================================================
# Path 
#==============================================================================

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Absolute filesystem path to project container folder:
PROJECT_ROOT = dirname(SITE_ROOT) 

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
# Database Configuration
#==============================================================================
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DJANGO_DB_NAME', ''),
        'USER': os.environ.get('DJANGO_DB_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': 'localhost',
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
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'static')),
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
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'uploads'))

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
    'social_auth.context_processors.social_auth_by_name_backends',
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
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
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

AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'account.auth_backends.UsernameAuthenticationBackend',
    "phileo.auth_backends.CanLikeBackend",
)

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_LOGIN_REDIRECT_URL = 'profiles_profile_login'
ACCOUNT_SIGNUP_REDIRECT_URL = 'profiles_profile_login'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

LOGIN_URL = reverse_lazy('account_login')
LOGIN_REDIRECT_URL = reverse_lazy('profiles_profile_login')

# Social Auth

LOGIN_ERROR_URL = "/account/social/connections/"
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = False
SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account/social/connections'

SOCIAL_AUTH_PIPELINE = [
    "libs.pipeline.prevent_duplicates",
    "social_auth.backends.pipeline.social.social_auth_user",
    "social_auth.backends.pipeline.user.get_username",
    "social_auth.backends.pipeline.user.create_user",
    "social_auth.backends.pipeline.social.associate_user",
    "social_auth.backends.pipeline.social.load_extra_data",
    "social_auth.backends.pipeline.user.update_user_details",
    "libs.pipeline.get_user_avatar",
    "libs.pipeline.update_user_profile"
]

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", "")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", "")

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", "")
FACEBOOK_API_SECRET = os.environ.get("FACEBOOK_API_SECRET", "")
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
    'django.contrib.gis',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # autocomplete forms
    'autocomplete_light'
)

THIRD_PARTY_APPS = (
    'south', # database migrations
    'gunicorn', # server
    'djcelery', # async
    'djsupervisor', # process mgmt
    
    'account', # local accounts
    'social_auth', # social accounts

    'compressor', # static file optimization
    'pagination', # pagination
    'easy_thumbnails', # image manipulation
    
    'taggit', # tagging
    'metron', # analytics
    'phileo', # liking
    'actstream', # activity stream, following

    'rest_framework', # api
    'rest_framework_gis', # api geo add-ons
    
    'floppyforms', # form tools
    'django_js_reverse' # javascript url tools
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.about', # about page
    'apps.core', # general helpers
    #'apps.text', # blog
    'apps.comments', # comments
    'apps.profiles', # user profiles
    'apps.ideas', # user uploaded ideas
    'apps.lotxlot', # lots
    'apps.philadelphia', # philly data
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
# Server Configuration
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

SERVER_PORT = os.environ.get("SERVER_PORT", "8000")

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
# Caching
#==============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/possiblecity/memcached.sock',
        'TIMEOUT': 300,
    }
}


#==============================================================================
# ASync
#==============================================================================

BROKER_URL = "redis://localhost:6379/0"

# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://docs.celeryproject.org/en/master/configuration.html#std:setting-CELERY_CHORD_PROPAGATES
CELERY_CHORD_PROPAGATES = True

# See: http://celery.github.com/celery/django/
setup_loader()

#==============================================================================
# API
#==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGINATE_BY': 10
}


#==============================================================================
# Other 3rd Party
#==============================================================================

PHILEO_DEFAULT_LIKE_CONFIG = {
    "css_class_on": "icon-star",
    "css_class_off": "icon-star-empty",
    "like_text_on": "Favorited",
    "like_text_off": "Favorite",
    "count_text_singular": "favorite",
    "count_text_plural": "favorites"
}


PHILEO_LIKABLE_MODELS = {
    "profiles.Profile": {},
    "ideas.Idea": {},
    "lotxlot.Lot": {},
    "comments.Comment": {}
}

ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'lotxlot.lot', 'ideas.idea', 'phileo.like', 'comments.comment'),
    'USE_PREFETCH': True,
}


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
    'PAPL_PARCELS': 'http://gis.phila.gov/ArcGIS/rest/services/RDA/PAPL_Web/MapServer/2/',
    'PAPL_WEB':	'http://secure.phila.gov/PAPLPublicWeb/',
    'SERVICE_ZIP': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/24/',
    'SERVICE_PHILLYRISING': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/16/',
    'SERVICE_COUNCIL': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/2/',
    'SERVICE_PLANNING': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/21/',
    'SERVICE_CENSUS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/0/',
    'SERVICE_BLOCKGROUP': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/1/',
    'SERVICE_WARD': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ServiceAreas/MapServer/11/',
    'VACANCY': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/', 
    'VACANCY_APPEALS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/0/',
    'VACANCY_LICENSES': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/2/',
    'VACANCY_DEMOLITIONS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/4/',
    'VACANCY_DEMOLITION_PERMITS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/6/',
    'VACANCY_VIOLATIONS': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/Vacancy/MapServer/8/',
    'ZONING_BASE': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ZoningMap/MapServer/6/',
    'ZONING_OVERLAY': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ZoningMap/MapServer/1/',
    'ZONING_FLOOD': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ZoningMap/MapServer/3/',
    'ZONING_SLOPE': 'http://gis.phila.gov/ArcGIS/rest/services/PhilaGov/ZoningMap/MapServer/2/',
}
