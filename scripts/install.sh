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
pip install -r backend/requirements.txt

# Создаем БД
echo Creating database...
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER --set=DB_NAME=$DB_NAME -f scripts/init_db.sql

# Выполняем миграции
python backend/manage.py migrate

# Создаем индексы для текстового поиска
echo Creating database indexes...
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER --set=DB_NAME=$DB_NAME -f scripts/create_db_index.sql

# Собираем статику
python backend/manage.py collectstatic

# Подставляем путь до проекта в конфиги и скрипты
echo Configure project path and domain...
sed -i "s~template_path~$project_path~g" nginx/kmsjob.conf systemd/kmsjob.gunicorn.service
sed -i "s~template_domain~$project_domain~g" nginx/kmsjob.conf
sed -i "s~template_path~$project_path~g" scripts/crontab

# Подключаем сервера
echo Enable servers...
sudo ln -fns $project_path/nginx/kmsjob.conf /etc/nginx/sites-enabled/
sudo ln -fns $project_path/systemd/kmsjob.gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start kmsjob.gunicorn
sudo systemctl enable kmsjob.gunicorn
sudo service nginx restart

# Настраиваем HTTPS
sudo certbot --nginx -d $project_domain

# Добавляем задания в cron
crontab scripts/crontab

echo Project installed! Check https://$project_domain