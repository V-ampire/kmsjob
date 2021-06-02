#!/bin/bash
base_python_interpreter=""
project_domain=""
project_path=`pwd`

# Загрузить переменные окружения
export $(xargs < backend/.env)

# Задать интерпритатор Python
read -p "Python interpreter: " base_python_interpreter

# Домен сайта
read -p "Your domain without protocol (for example, google.com): " project_domain

# Создаем виртуальное окружение
`$base_python_interpreter -m venv backend/env`
source backend/env/bin/activate
pip install -U pip
pip install -r requirements.txt

# Создаем БД
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER --set=DB_NAME=$DB_NAME -f scripts/init_db.sql

# Выполняем миграции
pytnon backend/manage.py migrate

# Создаем индексы для текстового поиска
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER --set=DB_NAME=$DB_NAME -f shell_scripts/create_db_index.sql

# Собираем статику
pytnon backend/manage.py collectstatic

# Подставляем путь до проекта в конфиги и скрипты
sed -i "s~template_path~$project_path~g" nginx/site.conf systemd/gunicorn.service
sed -i "s~template_domain~$project_domain~g" nginx/site.conf
sed -i "s~template_path~$project_path~g" scripts/run_parsers.sh
sed -i "s~template_path~$project_path~g" scripts/run_cleaner.sh

# Подключаем сервера
sudo ln -s $project_path/nginx/site.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/systemd/gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo service nginx restart

# Настраиваем HTTPS
sudo certbot --nginx -d $project_domain

# Добавляем задания в cron
chmod -R ug+x scripts/*
# Парсить новые вакансии каждый день в 10-00
0 10 * * * $project_path/scripts/run_parsers.sh >> scripts/crontab.txt
# Запускать удаление старых вакансии каждый день в 10-01
01 10 * * * $project_path/scripts/run_cleaner.sh >> scripts/crontab.txt

crontab scripts/crontab.txt

echo Project installed! Check $project_domain