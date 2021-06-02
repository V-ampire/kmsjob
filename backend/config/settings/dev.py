from .base import *


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'telegram': {
            'class': 'telegram_logger.TelegramStreamHandler',
            'chat_ids': env.list('CHAT_IDS'),
            'token': env('TG_TOKEN'),
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'telegram': {
            'handlers': ['telegram'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
