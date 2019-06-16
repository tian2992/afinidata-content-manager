from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default',
    },
    'messenger_users_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'messengeruser',
    }
}
    
