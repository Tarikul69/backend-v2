import os
from django.contrib.messages import constants as messages
from pathlib import Path

#pip list --format=freeze > requirements.txt
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# os.environ['SENDGRID_API_KEY'] = 'SG.mI1AY8QGQFq5MT8d0fsl-Q.JHbc55MX0UAbC0UHcJJgqrvGpAnitFAlUlbS0jq8lVU'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_qe@gsur0xdvgu4cif&q_+nc4o1os15%(8t%j6u3tm0xvwrn6#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App.apps.AppConfig',
    'tinymce',
    'multiselectfield',
    'awesome_django_timezones'
]

TINYMCE_DEFAULT_CONFIG = {
    "menubar": "file edit view insert format tools table",
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount,spellchecker",
    "height": 350
}
TINYMCE_SPELLCHECKER = True



IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE_CLASSES = (
    'awesome_django_timezones.middleware.TimezonesMiddleware',
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'ExamPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ExamPortal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oes',
        'USER': 'admin2',
        'PASSWORD': '1234',
        'HOST': '161.97.79.224',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'


USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Asia/Kolkata'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_file')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mailuser3008@gmail.com'
EMAIL_HOST_PASSWORD = 'ewegqnvkguiwtbdx'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@engagenreap.com'



MESSAGE_TAGS = {
    messages.DEBUG : "alert-primary",
    messages.SUCCESS:"alert-success",
    messages.ERROR:"alert-danger",
    messages.INFO:"alert-info",
    messages.WARNING:"alert-warning",
}
