"""
Django settings for snc project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's()bs57t5!cc-x9vt(uj&gupcm7qujam9v$ifamf(dg=)8+pjb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '.cultura.gov.br'
    ]
SITE_ID = 1

# Login configuration
LOGIN_REDIRECT_URL = '/adesao/home'
LOGIN_URL = '/adesao/login'
LOGOUT_URL = '/adesao/sair'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# E-mail configuration
DEFAULT_FROM_EMAIL = 'naoresponda@cultura.gov.br'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'correio.cultura.gov.br'
    # EMAIL_PORT = 25
    # EMAIL_TIMEOUT = 30


# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    )

THIRD_PARTY_APPS = (
    'widget_tweaks',
    'wkhtmltopdf',
    'smart_selects',
    'localflavor',
    'django_extensions',
    'ckeditor',
    'piwik',
    'clever_selects',
    'rest_framework',
    'django_filters',
    'rest_framework_swagger',
    'drf_hal_json' 
    )


LOCAL_APPS = (
    'snc',
    'adesao',
    'planotrabalho',
    'gestao',
    'api'
    )

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.HalLimitOffsetPagination',
    'PAGE_SIZE': 1,
    'DEFAULT_PARSER_CLASSES': ('drf_hal_json.parsers.JsonHalParser',),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_hal_json.renderers.JsonHalRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    
    ),

    'URL_FIELD_NAME': 'self',
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    )

ROOT_URLCONF = 'snc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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

WSGI_APPLICATION = 'snc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbsnc',
        # 'NAME': 'dbsnc',
        # 'USER': 'usr_snc',
        'USER': 'postgres',
        'PASSWORD': '123456',
        # 'PASSWORD': 'KA4UGbLxX78GJoL',
        # 'PASSWORD': 'snc',
        # 'HOST': '10.0.0.217',
        # 'HOST': '10.0.0.229',
        # 'HOST': '10.0.0.230',
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
def ABS_DIR(rel):
    return os.path.join(BASE_DIR, rel.replace('/', os.path.sep))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

# Smart selects
USE_DJANGO_JQUERY = False
JQUERY_URL = STATIC_URL + 'js/jquery.min.js'

# CKEditor
CKEDITOR_JQUERY_URL = JQUERY_URL
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
            ]
        },
    }

# Piwik
PIWIK_SITE_ID = 16
PIWIK_URL = 'https://analise.cultura.gov.br/'
