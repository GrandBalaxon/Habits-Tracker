# Habits-Tracker

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.17-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue.svg)
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

## Требования

- Python 3.14+
- Poetry
- Docker и Docker Compose (для контейнеризации)
- PostgreSQL (локально или через Docker)
- Redis (локально или через Docker)
- Telegram Bot Token (для отправки уведомлений)


## Локальный запуск

1. Убедитесь, что у вас установлены требуемые программы
2. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/GrandBalaxon/Habits-Tracker.git
    cd Habits-Tracker
    ```
3. Создайте и заполните `.env` (на основе `.env.template`). 
4. Установка зависимостей через `Poetry`:
    ```bash
    poetry install
    ```
5. Убедитесь, что PostgreSQL и Redis запущены локально, либо поднимите их в Docker (рекомендуется для простоты).
6. Применение миграций
    ```bash
    python manage.py migrate
    ```
7. Создание суперпользователя (опционально)
    ```bash
    python manage.py createsuperuser
    ```
8. Запуск сервера разработки
    ```bash
    python manage.py runserver
    ```
   Проект будет доступен по адресу http://localhost:8000/.
9. Запуск Celery worker и Celery beat (для уведомлений)
    В отдельных терминалах выполните:
    ```bash
    celery -A config worker -l info
    celery -A config beat -l info
    ```

## Локальный запуск (через Docker)

Альтернативно, можно развернуть все сервисы (web, db, redis, celery_worker, celery_beat, nginx) одной командой:

```bash
docker compose up -d --build
```

Перед этим убедитесь, что в `.env` указаны правильные параметры: 
для Docker-окружения **POSTGRES_HOST=db**, а **CELERY_BROKER_URL=redis://redis:6379**. 
Можно также использовать переопределение через `environment` в docker-compose.yml.

После запуска проверьте статус контейнеров:

```bash
docker compose ps
```


## CI/CD и деплой на сервер

Проект включает конфигурацию GitHub Actions для автоматической проверки кода и деплоя на сервер.

### Структура workflow

Workflow запускается при push в ветку main и pull request. Он состоит из четырёх этапов:

1. `lint` — запуск Flake8 для проверки стиля кода.
2. `test` — запуск тестов Django.
3. `build` — сборка Docker-образа для проверки корректности Dockerfile.
4. `deploy` — (только для push в main) подключение к серверу по SSH, обновление кода и перезапуск контейнеров.

### Настройка секретов GitHub

Для работы пайплайна необходимо добавить секреты в репозиторий (Settings → Secrets and variables → Actions):

* `SECRET_KEY` — секретный ключ Django (используется в тестах).
* `SSH_KEY` — приватный SSH-ключ для доступа к серверу.
* `SSH_USER` — имя пользователя на сервере.
* `SERVER_IP` — IP-адрес сервера.

### Настройка SSH-доступа

1. Сгенерируйте SSH-ключ (если ещё нет) на локальной машине:
    ```bash
    ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
    ```
2. Добавьте публичный ключ (`~/.ssh/github_actions_deploy.pub`) в `~/.ssh/authorized_keys` на сервере:
    ```bash
    ssh-copy-id -i ~/.ssh/github_actions_deploy.pub ваш_пользователь@IP_сервера
    ```
3. Скопируйте приватный ключ (`~/.ssh/github_actions_deploy`) в секрет `SSH_KEY` на **GitHub**.
4. Укажите `SSH_USER` и `SERVER_IP` в секретах.

### Настройка сервера

1. Установите `Docker` и `Git` на сервер
2. Клонируйте репозиторий:
    ```bash
    cd /home/$USER
    git clone https://github.com/GrandBalaxon/Habits-Tracker.git
    cd Habits-Tracker
    ```
3. Создайте и заполните `.env` (на основе `.env.template`). 
    ```bash
    cp .env.template .env
    nano .env
    ```
4. Запустите сборку и запуск всех контейнеров:
    ```bash
    docker compose up -d --build
    ```
5. При необходимости выполните миграции вручную (если сервис migrate не запускается автоматически или вы хотите убедиться):
    ```bash
    docker compose exec web python manage.py migrate
    ```
6. Проверьте состояние всех контейнеров:
    ```commandline
    docker compose ps
    ```
   Все сервисы (`db`, `redis, web`, `celery_worker`, `celery_beat`, `nginx`) должны находиться в состоянии `Up`.
7. Откройте приложение в браузере по адресу `http://<IP-сервера>/` (Nginx слушает порт 80). Если вы используете домен, настройте его в nginx/nginx.conf и перезапустите Nginx:
    ```bash
    docker compose restart nginx
    ```

После выполнения этих шагов проект будет полностью развёрнут на сервере. Если вы настроили CI/CD, деплой будет выполняться автоматически при каждом пуше в ветку `main`.


## 📜 Лицензия

Этот проект распространяется под лицензией MIT.