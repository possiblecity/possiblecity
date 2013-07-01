DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


SECRET_KEY = "thzz)o&he%w%5oagz4d0ujr$d)4cxsta1z&hrt%-01-4(zsqih"
