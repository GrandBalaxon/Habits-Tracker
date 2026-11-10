![Habits-Tracker — Small steps. Better habits. Напоминание: читать перед сном дома в 22:23.](docs/assets/readme-banner.jpg)


[![Django CI](https://github.com/GrandBalaxon/Habits-Tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/GrandBalaxon/Habits-Tracker/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/GrandBalaxon/Habits-Tracker/python-coverage-comment-action-data/badge.svg)](https://github.com/GrandBalaxon/Habits-Tracker/tree/python-coverage-comment-action-data)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.18-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![Celery](https://img.shields.io/badge/celery-5.7-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📝 О проекте

**Habits-Tracker** — бэкенд SPA-приложения для формирования и отслеживания полезных привычек по мотивам книги Джеймса Клира «Атомные привычки». Пользователи могут указывать место, время и действие, а также выбирать материальное вознаграждение или связанную приятную привычку.

Сервис предоставляет REST API, отправляет напоминания через Telegram-бота и позволяет авторизованным пользователям просматривать публичные привычки других пользователей.

*Стилизованный пример уведомления в Telegram (не скриншот):*

<img src="docs/assets/telegram-reminder.png" width="480" alt="Пример уведомления: читать книгу дома в 22:23 в течение 60 секунд, повторять через 24 часа; награда — 90 секунд сериала на диване в 22:24.">


## 🛠️ Возможности проекта

- **Пользователи** — регистрация, JWT-аутентификация и управление своим профилем.
- **Привычки** — создание, просмотр, редактирование и удаление, разделение на полезные и приятные.
- **Проверки данных** — валидация продолжительности, периодичности, вознаграждения и связанной привычки на уровне API.
- **Публичные привычки** — отдельный список привычек других пользователей, доступный после авторизации.
- **Telegram-уведомления** — планирование напоминаний с помощью Celery и Redis.
- **Документация API** — интерактивный Swagger UI и схема OpenAPI.
- **Docker Compose** — PostgreSQL, Redis, Django, Celery worker, Celery beat и Nginx.
- **CI/CD** — линтер, проверки Django и миграций, тесты с coverage и сборка образов.

## 📖 Документация и запуск

Руководство по установке и запуску содержит настройку окружения, запуск через Docker и Poetry, проверку API, инструкции для тестов, демонстрационных данных и CI/CD.

👉 **[Перейти к руководству](docs/SETUP.md)**

## 🔗 Основные маршруты

| Маршрут | Назначение |
| --- | --- |
| `/api/docs/` | Swagger UI |
| `/api/schema/` | Схема OpenAPI |
| `/admin/` | Административный интерфейс Django |
| `/user/create/` | Регистрация пользователя |
| `/token/`, `/token/refresh/` | Получение и обновление JWT |
| `/user/profile/`, `/user/habits/` | Профиль и собственные привычки |
| `/habit/list/`, `/habit/create/`, `/habit/<id>/` | Публичный список, создание и детали привычки |

Маршруты и методы доступны в Swagger UI.

## 📜 Лицензия

Проект распространяется под [лицензией MIT](LICENSE).
