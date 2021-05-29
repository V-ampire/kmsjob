import os
import environ
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_FILE = os.path.join(BASE_DIR, '.env')

env = environ.Env()
environ.Env.read_env(env_file=ENV_FILE)

SITE_ID = 1

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'vacancies',
    'feedback'
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'


PARSERS_CONFIG = {
    "superjob": {
        "parse_url": "https://api.superjob.ru",
        "base_url": "https://superjob.ru",
        "secret_key": env.str('SJ_SECRET_KEY'),
        "id": 1091,
        "v": "2.0",
        "is_active": True
    },
    "avito": {
        "parse_url": "https://www.avito.ru/komsomolsk-na-amure/vakansii?s=104&s_trg=11",
        "base_url": "https://www.avito.ru",
        "is_active": True
    },
    "farpost": {
        "parse_url": "https://www.farpost.ru/komsomolsk-na-amure/job/vacancy/",
        "base_url": "https://www.farpost.ru",
        "is_active": True
    },
    "hh": {
        "parse_url": "https://api.hh.ru/vacancies/",
        "base_url": "https://hh.ru",
        "is_active": True
    },
    "vk": {
        "parse_url": "https://api.vk.com/method/newsfeed.search",
        "base_url": "https://vk.com",
        "client_id": env.str('VK_CLIENT_ID'),
        "access_token": env.str('VK_ACCESS_TOKEN'),
        "v": 5.95,
        "is_active": True
    }
}

VACANCY_EXPIRE = timedelta(weeks=4*3) # Очищать вакансии каждые 3 месяца