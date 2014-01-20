# settings/production.py

import os

from django.core.exceptions import ImproperlyConfigured

from celery.schedules import crontab

from base import *


#==============================================================================
# Site
#==============================================================================
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['possiblecity.co', 'www.possiblecity.co', 'smtp.webfaction.com']


#==============================================================================
# Email
#==============================================================================
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.webfaction.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = 'possiblecity'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = '587'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_USE_TLS = 'True'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'admin@possiblecity.co'

DEFAULT_FROM_EMAIL = 'Possible City <info@possiblecity.co>'


#==============================================================================
# Installed Apps
#==============================================================================

INSTALLED_APPS += (
    'memcache_status',
)

#==============================================================================
#  Celery
#==============================================================================


BROKER_URL = 'redis://localhost:14484/0'
CELERY_RESULT_BACKEND = 'database'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_PIDFILE = '/tmp/celerybeat.pid'
CELERYBEAT_SCHEDULE = {} # Will add tasks later
