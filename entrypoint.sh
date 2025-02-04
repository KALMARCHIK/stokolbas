#!/bin/sh
set -e  # Остановить выполнение, если есть ошибка

# Ждем, пока БД станет доступна
echo "Ожидание запуска базы данных..."
while ! nc -z db 5432; do
  sleep 1
done
echo "База данных запущена!"

# Применяем миграции
echo "Применение миграций..."
python manage.py migrate --noinput

# Создаем суперпользователя, если его нет
echo "Создание суперпользователя..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'superuser')
EOF

# Запускаем команду, переданную в контейнере (gunicorn)
exec "$@"