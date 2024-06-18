# Телеграм-БОТ для оповещения пользователей в сервисе бронирования коворкингов УрФУ

## Переменные окружения

```bash
# Bot config
BOT_TOKEN=...
LOG_LEVEL=...

# Database config
DATABASE_USER=...
DATABASE_PASSWORD=...
DATABASE_HOST=...
DATABASE_PORT=...
DATABASE_NAME=...

# SMTP config
SMTP_EMAIL=...
SMTP_PASSWORD=...
SMTP_SERVER=...
SMTP_PORT=...
```

## Запуск приложения

* Запустите сборку Docker-образа

```bash
make build
```

* Запустите приложение

В корневой директории должен быть создан .env файл с переменными окружениями

```bash
make run
```
