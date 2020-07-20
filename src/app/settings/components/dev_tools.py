import os
from app.settings.components.base import INSTALLED_APPS, MIDDLEWARE, BASE_DIR

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}


INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"
FIXTURE_DIRS = (os.path.join(BASE_DIR, 'tests/fixtures'),)