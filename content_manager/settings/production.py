from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']
DOMAIN_URL = 'https://contentmanager.afinidata.com'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('CM_DATABASE_ENGINE'),
        'NAME': os.getenv('CM_DATABASE_NAME'),
        'USER': os.getenv('CM_DATABASE_USER'),
        'PASSWORD': os.getenv('CM_DATABASE_PASSWORD'),
        'HOST': os.getenv('CM_DATABASE_HOST'),
        'PORT': os.getenv('CM_DATABASE_PORT'),
    },
    'messenger_users_db': {
        'ENGINE': os.getenv('CM_DATABASE_ENGINE'),
        'NAME': os.getenv('CM_DATABASE_USERS_NAME'),
        'USER': os.getenv('CM_DATABASE_USER'),
        'PASSWORD': os.getenv('CM_DATABASE_PASSWORD'),
        'HOST': os.getenv('CM_DATABASE_HOST'),
        'PORT': os.getenv('CM_DATABASE_PORT'),
    }
}