from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured
import mysql_setting

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets = secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable 카톡에 씨크릿키 파일 있음. 깃이그노어 있는 폴더에 붙여넣엉".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    ".ap-northeast-2.compute.amazonaws.com",
    ".fromnode.com",
    '127.0.0.1',
    '3.34.187.248',
    '13.125.160.94',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MainApp',
    'NodeApp',
    'ProjectApp',
    'UserApp',
    'FileApp',
    # 'NotificationApp',
    'sass_processor',
    'notifications',
    'colorfield',
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

ROOT_URLCONF = 'FromNode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'MainApp/templates/Base')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'MainApp.context_processors.project_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'FromNode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = mysql_setting.DATABASES



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = (
    '/MainApp/static/',
    '/NodeApp/static/',
    '/ProjectApp/static/',
    '/UserApp/static/',
    '/FileApp/static',
    # '/baseTemplates/static/',
)
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]
SASS_PROCESSOR_ROOT = STATIC_ROOT
SASS_PROCESSOR_ENABLED = True
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = 'compact'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
