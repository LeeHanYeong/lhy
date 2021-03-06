"""
Django settings for lhy project.
Generated by 'django-admin startproject' using Django 2.2.7.
"""
import os

from aws_secrets import SECRETS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
LOG_DIR = os.path.join(ROOT_DIR, '.log')
TEMP_DIR = os.path.join(ROOT_DIR, '.temp')
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

ALLOWED_HOSTS = []

# django-aws-secrets-manager
AWS_SECRETS_MANAGER_SECRETS_NAME = 'lhy'
AWS_SECRETS_MANAGER_PROFILE = 'lhy-secrets-manager'
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'lhy:base'
AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'
SECRET_KEY = SECRETS['SECRET_KEY']

# django-storages
AWS_S3_ACCESS_KEY_ID = SECRETS['AWS_S3_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = SECRETS['AWS_S3_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = 'private'
AWS_BUCKET_ACL = 'private'
AWS_AUTO_CREATE_BUCKET = True

# django-dbbackup
DBBACKUP_STORAGE = 'config.storages.DBStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': SECRETS['AWS_S3_ACCESS_KEY_ID'],
    'secret_key': SECRETS['AWS_S3_SECRET_ACCESS_KEY'],
}

# Auth
AUTH_USER_MODEL = 'members.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'apps.members.backends.SettingsBackend',
]
LOGIN_REDIRECT_URL = 'index'
DEFAULT_USERS = {
    'dev@lhy.kr': {
        'password': 'pbkdf2_sha256$150000$89oDFBSARLc8$Jsv1BlODbmILIiENOq3/2cvQM4663zW+clxzm52Fo28=',
        'name': '이한영',
        'type': 'email',
        'is_staff': True,
        'is_superuser': True,
    },
}

# django-allauth
SITE_ID = 1

# Static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATICFILES_DIRS = [STATIC_DIR]

# Date/Time Format
DATE_FORMAT = 'Y년 m월 d일'
TIME_FORMAT = 'H시 i분'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'utils.drf.renderers.BrowsableAPIRendererWithoutForms',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    'EXCEPTION_HANDLER': 'utils.drf.exceptions.custom_exception_handler',
}

# drf-yasg
TOKEN_DESCRIPTION = '''
### [DRF AuthToken](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
인증정보를 사용해 [AuthToken](#operation/auth_token_create) API에 요청, 결과로 돌아온 **key**를  
HTTP Request의 Header `Authorization`에 `Token <key>`값을 넣어 전송

```
Authorization: Token fs8943eu342cf79d8933jkd
``` 
'''
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'DRF AuthToken',
            'description': TOKEN_DESCRIPTION,
        }
    }
}

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'KR'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# easy-thumbnails
THUMBNAIL_DEFAULT_STORAGE = 'config.storages.MediaStorage'
THUMBNAIL_WIDGET_OPTIONS = {
    'size': (300, 300),
}
THUMBNAIL_ALIASES = {
    '': {
        'admin_list': {'size': (100, 100), 'crop': False},
    },
}

# django-modeladmin-reorder
ADMIN_REORDER = (
    {'app': 'members', 'label': '사용자 관리', 'models': (
        {'model': 'members.User', 'label': '사용자'},
    )},
    {'app': 'polls', 'label': '설문조사 관리', 'models': (
        {'model': 'polls.Poll', 'label': '설문조사'},
        {'model': 'polls.Choice', 'label': '선택지'},
        {'model': 'polls.Vote', 'label': '투표'},
    )},
)

# Apps
USER_APPS = [
    'apps.members',
    'apps.polls',
]
PYPI_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'admin_reorder',
    'adminsortable2',
    'dbbackup',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
    'django_filters',
    'drf_yasg',
    'rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'phonenumber_field',
    'polymorphic',
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]
INSTALLED_APPS = USER_APPS + PYPI_APPS + DJANGO_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(TEMPLATES_DIR, 'jinja2')],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'config.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s'
        },
    },
    'handlers': {
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'default',
            'maxBytes': 1048576,
            'backupCount': 10,
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'formatter': 'default',
            'maxBytes': 1048576,
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'file_error',
                'file_info',
                'console',
            ],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
