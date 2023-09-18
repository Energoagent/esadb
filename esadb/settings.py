import os

from pathlib import Path

def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except:
        return ''
        
DJANGO_CONFIG = get_env_value('django_config')

DJANGO_DEBUG = get_env_value('django_debug')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'django-insecure-5b=(k-uws^(_7%c23e4pdx225*y$2*^i4q^qpo45pi^cmw+%1('

DEBUG = DJANGO_DEBUG == 'true'
#DEBUG = True


ALLOWED_HOSTS = [
    'askue.energoagent.com',
    'esadb.energoagent.com',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'esadbsrv',
    'albumstore',
    'docstore',
    'einst',
    'org',
    'contact',
    'channel',
    'project',
    'ttnexample',
    'meter',
    'commdevice',
    'mic',
    'gdiskstorage',
    'nxcstorage',
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
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'docstore.middleware.ds_middleware',
    'albumstore.middleware.as_middleware',
    'esadbsrv.middleware.middleware',
    'org.middleware.middleware',
    'einst.middleware.middleware',
    'contact.middleware.middleware',
    'channel.middleware.middleware',
#    'gdiskstorage.middleware.middleware',
#    'nxcstorage.middleware.middleware',
]

ROOT_URLCONF = 'esadb.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
            os.path.join(BASE_DIR, 'contact/templates'),
            os.path.join(BASE_DIR, 'channel/templates'),
            os.path.join(BASE_DIR, 'docstore/templates'),
            os.path.join(BASE_DIR, 'org/templates'),
            os.path.join(BASE_DIR, 'albumstore/templates'),
            os.path.join(BASE_DIR, 'project/templates'),
            os.path.join(BASE_DIR, 'ttnexample/templates'),
            os.path.join(BASE_DIR, 'meter/templates'),
            os.path.join(BASE_DIR, 'commdevice/templates'),
            os.path.join(BASE_DIR, 'mic/templates'),
            os.path.join(BASE_DIR, 'gdiskstorage/templates'),
            os.path.join(BASE_DIR, 'esadbsrv/templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'esadbsrv.context_processors.contextinfo',
                'project.context_processors.projectcontext',
                'einst.context_processors.einstcontext',
            ],
        },
    },
]

WSGI_APPLICATION = 'esadb.wsgi.application'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

if DJANGO_CONFIG == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'esadb',
            'USER' : 'postgres',
            'PASSWORD' : 'Immelstorn',
            'HOST' : '127.0.0.1',
            'PORT' : '5433',
        }
    }
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    EXPORT_DIR = os.path.join(BASE_DIR, 'export/')
    IMPORT_DIR = os.path.join(BASE_DIR, 'import/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    MEDIA_URL = '/media/'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'django_project_db',
            'USER' : 'django',
            'PASSWORD' : 'ieshie7Xee4o',
            'HOST' : 'localhost',
            'PORT' : '',
        }
    }
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    MEDIA_URL = '/media/'


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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND ='django.core.mail.backends.console.EmailBackend'

#cloud settings
ASCLOUD_NAME = 'esadb.energoagent@mail.ru'
ASCLOUD_PASSWORD = 'VitybXegUNpyzs9bsPjr'
ASCLOUD_URL = 'https://cloud.mail.ru/home'

# Google drive settings
API_KEY= 'AIzaSyByrhPqSqzEVq3cX0ijqIkMnjZsKTFP1bY'



