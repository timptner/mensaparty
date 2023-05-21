import django

# noinspection PyPackageRequirements
from decouple import config
from dj_database_url import parse as db_url
from django.urls import reverse_lazy
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost',
    cast=lambda v: [s.strip() for s in v.split(',')],
)

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'workers',
    'reviews',

    'anymail',
    'fontawesomefree',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mensaparty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'mensaparty' / 'templates',
            django.__path__[0] + '/forms/templates',
        ],
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

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'mensaparty.wsgi.application'


# Database

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        cast=db_url,
    )
}


# Password validation

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

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'mensaparty' / 'static'
]

STATICFILES_STORAGE = config('STATIC_FILES_STORAGE', default='django.contrib.staticfiles.storage.StaticFilesStorage')

AWS_S3_ENDPOINT_URL = config('BUCKET_ENDPOINT_URL', default='')

AWS_STORAGE_BUCKET_NAME = config('BUCKET_NAME', default='')

AWS_ACCESS_KEY_ID = config('BUCKET_ACCESS_KEY', default='')

AWS_SECRET_ACCESS_KEY = config('BUCKET_SECRET_KEY', default='')

AWS_S3_CUSTOM_DOMAIN = config('BUCKET_DOMAIN', default='')


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# E-Mail

EMAIL_BACKEND = 'anymail.backends.postmark.EmailBackend'

DEFAULT_FROM_EMAIL = '"[Mensaparty] Fachschaftsrat Maschinenbau" <mensaparty@farafmb.de>'

SERVER_EMAIL = '"[Server] Fachschaftsrat Maschinenbau" <server@farafmb.de>'

ANYMAIL = {
    'POSTMARK_SERVER_TOKEN': config('POSTMARK_API_TOKEN'),
    'SEND_DEFAULTS': {
        'esp_extra': {
            'MessageStream': config('DEFAULT_STREAM', default='outbound'),
        },
    }
}


# Authentication

LOGIN_URL = reverse_lazy('admin:login')
