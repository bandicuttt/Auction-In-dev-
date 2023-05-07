from pathlib import Path
from datetime import timedelta

import environ
import os

root = environ.Path(__file__) - 2
env = environ.Env()

environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()


SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'knox',
]

# apps

INSTALLED_APPS += [
    'users',
    'auctions',
]

AUTH_USER_MODEL='users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.errors_handler.errors_responses.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication','rest_framework.authentication.BasicAuthentication',),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

APPEND_SLASH=False

REST_KNOX = {
    'USER_SERIALIZER': 'users.serializers.users.CreateUserSerializer',
    'TOKEN_TTL': timedelta(hours=48)
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB', 'postgres'),
        'USER': env.str('POSTGRES_USER', 'postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', 'postgres'),
        'HOST': env.str('POSTGRES_HOST', 'db'),
        'PORT': env.int('POSTGRES_PORT', 5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Wallet',
        'DESCRIPTION': 'PixelCardWallet',
    'VERSION': '1.0.0',
    
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.AllowAny',
    ],
    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,

    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False

# cache
REDIS_HOST = env.str('REDIS_HOST','redis')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:6379',
        'OPTIONS': {
            'db':'1',
        }
    }
}

# celery
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = env.int('EMAIL_PORT', 465)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', True)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', '')
EMAIL_REDIRECT_DOMAIN = env.str('EMAIL_REDIRECT_DOMAIN','')
