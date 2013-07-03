# settings/base.py

from os.path import abspath, basename, dirname, join, normpath
from sys import path


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
# Manager 
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

INTERNAL_IPS = [
    '127.0.0.1',
]

#==============================================================================
# Secret Key 
#==============================================================================

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = r'{{ secret_key }}'


#==============================================================================
# Localization
#==============================================================================

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False    #internationalization machinery
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
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
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
    'pagination.middleware.PaginationMiddleware'
)


#==============================================================================
# Project URLS
#==============================================================================


# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'conf.urls'


#==============================================================================
# Messages
#==============================================================================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


#==============================================================================
# Authentication
#==============================================================================

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
#ACCOUNT_EMAIL_REQUIRED = False
#ACCOUNT_EMAIL_VERIFICATION ='mandatory'

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
    # Database migration helpers:
    'allauth', #authentication
    'allauth.account', #authentication
    'allauth.socialaccount', #authentication
    'allauth.socialaccount.providers.facebook', #authentication
    'allauth.socialaccount.providers.twitter', #authentication
    'compressor', # static file optimization
    'easy_thumbnails', # image manipulation
    'pagination', # pagination
    'south', # database migrations
    'taggit', # tagging
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.core', # general helpers
    'apps.text', # blog
    'apps.projects', # user generated projects
    'apps.profiles', # user profiles
    #'apps.lotxlot',
    #'apps.philadelphia',
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
