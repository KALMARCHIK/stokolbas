# Запуск

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
POSTGRES_DB=stokolbas
POSTGRES_USER=igsiggs
POSTGRES_PASSWORD=R4OyHyWz
DATABASE_URL=postgres://igsiggs:R4OyHyWz@db:5432/stokolbas
DEBUG=False
SECRET_KEY="django-insecure-pqhyu64gi!*ir*6&3)axn790=op$5$m)1)8=fm1yb#zi9@1jw+"
ALLOWED_HOSTS=217.114.3.6,stokolbas-stage.ru,www.stokolbas-stage.ru, 127.0.0.1
```

---

- Запуск контейнера Docker:

```
docker-compose up --build
```

---

- Стандартный пароль Admin:

```
Login: admin
Password: superuser
```

---
