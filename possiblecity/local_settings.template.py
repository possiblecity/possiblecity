# -*- coding: utf-8 -*-

LOCAL_DEV = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = (
    ('fooper','fooper@foo'),
)

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ABC'
EMAIL_HOST_PASSWORD = 'ABC'
EMAIL_USE_TLS = True

CACHE_BACKEND = 'locmem:///'
CACHE_MIDDLEWARE_SECONDS = 60*5
CACHE_MIDDLEWARE_KEY_PREFIX = 'mingus.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

INTERNAL_IPS = ('127.0.0.1',)

### DEBUG-TOOLBAR SETTINGS
DEBUG_TOOLBAR_CONFIG = {
'INTERCEPT_REDIRECTS': False,
}

#django-degug-toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

### django-markup
MARKUP_CHOICES = (
	'none',	
	'markdown',
	'textile',
	'restructuredtext',
)

TWITTER_CONSUMER_KEY = 'x9b7JDY7ccFpJFTJ9F7dQ'
TWITTER_CONSUMER_SECRET = '26oJOpL3DFE0UMv1hgnaBJIJkRyD28BXkglOtrTe20'
TWITTER_ACCESS_TOKEN_KEY = '399567821-gd3YuPJgLoZO1HzJk7rS5iO70h0W3pkptZDbbQIz'
TWITTER_ACCESS_TOKEN_SECRET = 'C9Mq5AdRQj0xSKQ5BLPNnNUnui9dgiO8aRfH64Ec'