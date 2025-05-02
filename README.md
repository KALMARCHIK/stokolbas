# Запуск.

- Клонируем репозиторий:

```
git clone https://github.com/cookie-rf/stokolbas.git
```

---

- Заходим в директорию:

```
cd stokolbas
```

---

- Заходим в директорию с проектом:

```
cd app
```

---

- Создаем .env файл (пример):

```

##################
# FOR PRODUCTION #
##################

ENV=production  
POSTGRES_DB=stokolbas
POSTGRES_USER=igsiggs
DATABASE_URL=postgres://igsiggs:R4OyHyWz@db:5432/stokolbas
DEBUG=False
SECRET_KEY="django-insecure-pqhyu64gi!*ir*6&3)axn790=op$5$m)1)8=fm1yb#zi9@1jw+"
ALLOWED_HOSTS=217.114.3.6,stokolbas-stage.ru,www.stokolbas-stage.ru,127.0.0.1


###################
# FOR DEVELOPMENT #
###################

ENV=development  
POSTGRES_DB=stokolbas
POSTGRES_USER=igsiggs
POSTGRES_PASSWORD=R4OyHyWz
POSTGRES_PORT=5432
DEBUG=True
SECRET_KEY="django-insecure-pqhyu64gi!*ir*6&3)axn790=op$5$m)1)8=fm1yb#zi9@1jw+"
ALLOWED_HOSTS=localhost,127.0.0.1

```

---

- Запуск контейнера Docker для локальной разработки:

```
docker-compose -f docker-compose.dev.yml up --build
```

---

- Остановка контейнера Docker для локальной разработки:

```
docker-compose -f docker-compose.dev.yml down -v
```

---

- Запуск контейнера Docker для продакшена:

```
docker-compose up --build
```

---

- Остановка контейнера Docker для продакшена:

```
docker-compose down -v
```

---

- Пароль Admin для локальной разработки:

```
Login: developer
Password: developer
```

---

- Пароль Admin для продакшена:

```
Login: admin
Password: superuser
```

---

### Добавление комбинатов

---

#### Калинковичский мясокомбинат

- Название: Каликовичский мясокомбинат (важно за каждым названием закреплен свой парсер)
- Сайт компании: https://kmk.by/catalog (ссылка должна быть на страницу с каталогом, там где категории)
- Прайс-лист: Файл excel с мясокомбината
  Дальше нажимаем "Обработать прайс-листы" и ждем сообщения
