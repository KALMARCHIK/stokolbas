# Используем Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями перед основным кодом (ускоряет сборку)
COPY requirements.txt /app/

# Устанавливаем зависимости
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
CMD ["gunicorn", "backend.wsgi:backend", "--bind", "0.0.0.0:8000"]
