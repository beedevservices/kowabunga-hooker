from pathlib import Path
import os
from environ import Env
from storeApp.keys import *

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'KEY'

DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['kowabunga-hooker.com']

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://kowabunga-hooker.com',
    # Add more allowed origins as necessary
]
CORS_ALLOWED_ALL_ORIGINS: True

X_FRAME_OPTIONS = "SAMEORIGIN"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storeApp.apps.StoreappConfig',
    'customerApp.apps.CustomerappConfig',
    'api.apps.ApiConfig',
    'theAdmin.apps.TheadminConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'kh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',
#         # 'ENGINE':'django.db.backends.mysql',
#         'NAME': 'thehives_hooker',
#         'USER': 'root',
#         # 'USER': 'craftsnh_hooker',
#         'PASSWORD': 'HoneyBee#4',
#         # 'PASSWORD': 'BeeDevKarg',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         # 'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_PORT = 465
EMAIL_HOST_USER = 'the.kowabunga.hooker@gmail.com'
# EMAIL_HOST_USER = 'kowabungahooker@gmail.com'
EMAIL_HOST_PASSWORD = HOST_PASSWORD
EMAIL_HOST_MAIN_USER = 'kaila@kowabunga-hooker.com'
EMAIL_HOST_ORDER_USER = 'orders@kowabunga-hooker.com'
