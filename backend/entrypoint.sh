#!/bin/sh

# Выйдите из скрипта при любой ошибке
set -e

echo "---------------- run prestart ----------------"

cd /app

echo "Backup db"
# Задержка нужна чтобы дождаться загрузки БД
sleep 10 
python cli.py dump

echo "Migrate db Alembic..."
alembic upgrade head || exit 1

echo "Run cron"
/usr/sbin/crond -b -l 8 -L /var/log/cron.log

echo "---------------- end prestart ----------------"

echo "Run APP..."
gunicorn app:create_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:80