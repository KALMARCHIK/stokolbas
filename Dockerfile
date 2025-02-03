# Используем Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию в контейнер
WORKDIR /app/backend

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


# Открываем порт (если нужно)
EXPOSE 8000

# Запускаем Django-сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]