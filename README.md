## Агрегатор вакансий города Комсомольска-на-Амуре.


**Это учебный проект на закреплений знаний по Django.**


Сайт доступен по адресу: [kmsjob.ru](https://kmsjob.ru)


## В проекте реализовано

- Сбор вакансий из источников
- Возможность добавления новых вакансий через форму обратной связи
- Сортировка вакансий по дате добавления, полнотекстовый поиск по вакансиям
- Логгирование ошибок в телеграм


## Деплой проекта

- Задать переменные окружения
```
DJANGO_SETTINGS_MODULE=
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DB_NAME=
DB_USER=
DB_PASSWORD=
SJ_SECRET_KEY=
VK_CLIENT_ID=
VK_ACCESS_TOKEN=
TG_TOKEN=
CHAT_IDS=
```

- Клонировать репозиторий `git clone https://github.com/V-ampire/kmsjob.git`

- Выполнить скрипт `scripts/isntall.sh`
