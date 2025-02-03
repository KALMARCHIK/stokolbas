#!/bin/sh

python manage.py migrate --noinput
python manage.py makemigrations 
python manage.py migrate 
             
echo "from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'superuser')" | python manage.py shell

exec "$@"