# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . /app/

# Даем права на выполнение entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn для продакшена
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
