# settings/staging.py

from os import environ

from production import *

DEBUG = True

#==============================================================================
# Site
#==============================================================================
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['possiblecity.webfactional.com',]

