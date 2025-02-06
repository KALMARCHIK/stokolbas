#!/bin/sh

# Выполняем миграции базы данных
python manage.py migrate --noinput
python manage.py makemigrations
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --noinput

# Создаем суперпользователя, если он не существует
echo "from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'superuser')" | python manage.py shell

exec "$@"
