from .base import *

# Secrets
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'washble:production'
DATABASES = SECRETS['DATABASES']

DEBUG = True
ALLOWED_HOSTS += ['*']
WSGI_APPLICATION = 'config.wsgi.production.application'

INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# django-debug-toolbar
INTERNAL_IPS = ['127.0.0.1']

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
