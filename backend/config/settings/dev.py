from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER' : env.str('DB_USER'),
        'PASSWORD' : env.str('DB_PASSWORD'),
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'telegram': {
            'class': 'telegram_logger.TelegramStreamHandler',
            'chat_ids': [1],
            'token': 'TOKEN',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'telegram_logger': {
            'handlers': ['telegram'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}