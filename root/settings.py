import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from import_export.formats.base_formats import XLSX, CSV

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["109.199.114.165", "127.0.0.1", "localhost", "217.77.4.131"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'import_export',
    'dal',
    'dal_select2',
    'admin_interface',
    'colorfield',
    'rosetta'
]

X_FRAME_OPTIONS = 'SAMEORIGIN'  # only if django version >= 3.0

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.languages'
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cargo_bot_db',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
        'PASSWORD': 1
    }
}

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

LANGUAGE_CODE = 'uz'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uz', _('Uzbek')),
    ('zh', _('Chinese')),
]

languages_dict = {
    "en": "English",
    "ru": "Russia",
    "uz": "Uzbek",
    'zh': "Chinese"
}

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/cargo_bot-master/root/cargo_admin/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT = True
IMPORT_EXPORT_FORMATS = [XLSX]
