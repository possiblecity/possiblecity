# settings/local.py
from .base import *

DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmeehan_possiblecity',
        'USER': 'dmeehan_possiblecity',
        'PASSWORD': '[0mplexc!ty',
        'HOST': '',
        'PORT': '',
    }
}

