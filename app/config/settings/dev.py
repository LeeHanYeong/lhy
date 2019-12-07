from .base import *

# Secrets
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'lhy:dev'
DATABASES = SECRETS['DATABASES']
DBBACKUP_STORAGE_OPTIONS['bucket_name'] = SECRETS['AWS_STORAGE_BUCKET_NAME']

DEBUG = True
ALLOWED_HOSTS += ['*']
WSGI_APPLICATION = 'config.wsgi.dev.application'

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
