# Habits-Tracker

[![Django CI](https://github.com/GrandBalaxon/Habits-Tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/GrandBalaxon/Habits-Tracker/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/GrandBalaxon/Habits-Tracker/python-coverage-comment-action-data/badge.svg)](https://github.com/GrandBalaxon/Habits-Tracker/tree/python-coverage-comment-action-data)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.17-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![Celery](https://img.shields.io/badge/celery-5.6-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📝 О проекте

**Habits-Tracker** — это бэкенд-часть SPA веб-приложения для формирования и отслеживания полезных привычек. Проект реализован на основе методологии, описанной в книге Джеймса Клира «Атомные привычки». Пользователи могут создавать привычки, указывая место, время и действие, а также выбирать способ вознаграждения: материальное поощрение или связанную приятную привычку.

Сервис предоставляет REST API, автоматически рассылает напоминания о выполнении привычек через Telegram-бота и позволяет делиться своими привычками с другими пользователями.

## 🛠️ Возможности проекта

- **Регистрация и аутентификация** — JWT-авторизация, управление профилем пользователя.
- **CRUD привычек** — создание, просмотр, редактирование и удаление привычек.
- **Полезные и приятные привычки** — разделение на два типа с возможностью связывания.
- **Гибкая валидация**:
  - время выполнения не более 120 секунд;
  - периодичность от 1 до 7 дней;
  - запрет одновременного указания вознаграждения и связанной привычки;
  - приятная привычка не может иметь вознаграждения или связанной привычки.
- **Публичные привычки** — просмотр привычек других пользователей без права редактирования.
- **Telegram-уведомления** — напоминания о начале привычки в заданное время.
- **Отложенные задачи Celery** — автоматическое планирование и перепланирование уведомлений с учётом периодичности.
- **Документация API** — Swagger / OpenAPI (drf-spectacular).
- **CORS-настройки** — безопасное подключение фронтенда.
- **Docker Compose** — контейнеризация всех сервисов: веб-приложение, Celery worker, Celery beat, PostgreSQL, Redis, Nginx.
- **CI/CD** — пайплайн GitHub Actions: линтинг, тестирование, сборка Docker-образа.

## 📖 Документация и запуск
Вся подробная информация по локальному запуску, настройке переменных окружения, развертыванию через Docker и загрузке тестовых данных перенесена в отдельное руководство:

👉 **[Перейти к руководству по установке и запуску](SETUP.md)**

## 📜 Лицензия

Этот проект распространяется под лицензией MIT.
