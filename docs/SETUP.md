# 🛠️ Руководство по установке и запуску

В этом руководстве описаны настройка Habits-Tracker, запуск через Docker или Poetry, работа с API и тестами. Команды рассчитаны на Bash-совместимую оболочку и выполняются из корня репозитория.

## Что потребуется

- Для **Docker-запуска**: Git, Docker Engine с плагином Docker Compose и свободный порт 80. Устанавливать Python, PostgreSQL и Redis на хост не требуется.
- Для **локального запуска**: Git, Python 3.14 или новее (но ниже 4.0), Poetry 2.2+ (рекомендуется 2.3.2, как в Docker), PostgreSQL и Redis. В CI используется Python 3.14.
- Для **Telegram-напоминаний** дополнительно нужен токен бота, Redis и работающие Celery worker и beat. Без них можно знакомиться с API, не включая уведомления.

Клонируйте репозиторий и перейдите в его каталог:

```bash
git clone https://github.com/GrandBalaxon/Habits-Tracker.git
cd Habits-Tracker
```

Дальнейшие инструкции относятся к версии проекта, содержащей этот файл и `config/settings_ci.py`.

## Переменные окружения

Создайте `.env`, если его ещё нет, и заполните его по образцу:

```bash
[ -f .env ] || cp .env.template .env
```

Пример **только для локальной разработки**; значения с `REPLACE` необходимо заменить:

```dotenv
DEBUG=True
SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET_KEY
POSTGRES_DB=habits
POSTGRES_USER=habits
POSTGRES_PASSWORD=REPLACE_WITH_A_DATABASE_PASSWORD
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
TELEGRAM_TOKEN=
CORS_ALLOW_ALL_ORIGINS=False
```

- `DEBUG` и непустой `SECRET_KEY` необходимы при загрузке настроек Django. Для каждого окружения используйте свой случайный ключ. Например, сгенерируйте его командой ниже и вставьте результат в `.env`:

  ```bash
  python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
  ```

- Для запуска Django на хосте заранее создайте PostgreSQL-базу и пользователя с указанными именем и паролем. Значения `POSTGRES_HOST` и `POSTGRES_PORT` должны указывать на доступный сервер.
- При запуске через Compose контейнер PostgreSQL создаёт базу и пользователя из `.env` при **первой** инициализации пустого тома. Изменение `.env` после этого не меняет автоматически уже созданные учётные данные.
- В Compose `POSTGRES_HOST` для приложения переопределяется значением `db`, а URL Redis для web, worker и beat — адресом `redis://redis:6379`. Оставьте `POSTGRES_PORT=5432`, если не меняли порт самого PostgreSQL внутри контейнера.
- `TELEGRAM_TOKEN` можно оставить пустым, пока уведомления не используются. `CORS_ALLOW_ALL_ORIGINS=True` разрешает все источники; используйте это только при необходимости в разработке. Списки `CORS_ALLOWED_ORIGINS` и `CSRF_TRUSTED_ORIGINS` сейчас заданы в `config/settings.py`, а не читаются из `.env`.

Не добавляйте `.env`, токен бота, пароли или приватные SSH-ключи в Git. `.dockerignore` исключает `.env` из контекста сборки, но Compose монтирует каталог проекта в web и Celery-контейнеры, поэтому файл доступен внутри этих контейнеров.

## Запуск через Docker Compose

1. Убедитесь, что `.env` заполнен, и соберите и запустите сервисы:

   ```bash
   docker compose up -d --build
   docker compose ps -a
   docker compose logs migrate
   ```

2. Проверьте, что `db`, `redis`, `web`, `celery_worker`, `celery_beat` и `nginx` работают, а одноразовый сервис `migrate` завершился с кодом 0. Если сервис web не запускается, проверьте логи миграций: `docker compose logs migrate`. Убедитесь, что миграции завершились успешно, и при необходимости запустите их вручную.

3. Откройте `http://localhost/api/docs/`. Nginx публикует порт 80; корневой URL `/` сам по себе может вернуть 404. При необходимости создайте администратора:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

Для диагностики используйте `docker compose logs web` или `docker compose logs celery_worker`. Остановить сервисы можно командой `docker compose down`: без флага `-v` именованные тома с данными сохраняются.

> PostgreSQL и Redis в текущем Compose-файле доступны другим контейнерам, но их порты не опубликованы на хост. Один только `docker compose up -d db redis` не обеспечит доступ к ним из запущенного на хосте Django без дополнительной настройки портов.

## Локальный запуск с Poetry

1. Установите зависимости в виртуальное окружение Poetry:

   ```bash
   poetry install --with dev,lint
   ```

   Если интерпретатор называется иначе, укажите путь к установленному Python 3.14 вместо `python3.14`. Команды ниже используют `poetry run`, поэтому активировать `.venv` вручную не нужно.

2. Заполните `.env`, подготовьте PostgreSQL-базу и убедитесь, что PostgreSQL доступен по адресу из файла. Для работы уведомлений запустите Redis на адресе из `CELERY_BROKER_URL` и `CELERY_RESULT_BACKEND`.

3. Примените миграции, при необходимости создайте администратора и запустите сервер:

   ```bash
   poetry run python manage.py migrate
   poetry run python manage.py createsuperuser  # необязательно
   poetry run python manage.py runserver
   ```

   Swagger UI: `http://localhost:8000/api/docs/`; админ-панель: `http://localhost:8000/admin/`.

4. Для Telegram-напоминаний запустите worker и beat в отдельных терминалах:

   ```bash
   poetry run celery -A config worker --loglevel=info
   ```

   ```bash
   poetry run celery -A config beat --loglevel=info
   ```

## API и Telegram

Swagger UI показывает маршруты и автоматически построенную схему API. Для ручной проверки используйте базовый адрес `http://localhost` при запуске через Compose или `http://localhost:8000` при локальном запуске Django.

Для ручного тестирования эндпоинтов (регистрация, получение JWT-токена, CRUD привычек) используйте встроенный Swagger UI по адресу /api/docs/. Не забудьте авторизоваться через кнопку Authorize, вставив Bearer <ваш_access_токен>.

* Список собственных привычек доступен по `GET /user/habits/`, а публичных привычек других пользователей — по `GET /habit/list/`. Для этих запросов требуется JWT-аутентификация.

* Обновить токен можно через `POST /token/refresh/`.

Для напоминаний укажите `TELEGRAM_TOKEN`, запустите Redis, worker и beat, а также задайте пользователю `telegram_chat_id` в админ-панели и включите `notifications_on` у привычки. Текущий API профиля не предоставляет поле `telegram_chat_id`; пользователь должен начать диалог с ботом. В настройках проекта и Celery используется часовой пояс `Europe/Moscow`.

## Демонстрационные данные

Фикстура [`habits/fixtures/initial_data.json`](habits/fixtures/initial_data.json) содержит пользователей и привычки. Она не требуется для автоматических тестов.

**Загружайте её только в отдельную локальную базу:** в ней есть учётная запись суперпользователя с хешем пароля и фиксированные ID. Совпадающие записи в существующей базе могут быть перезаписаны или вызвать конфликт. Не загружайте фикстуру в production и не используйте её учётные данные для реального доступа.

После миграций загрузите данные одним из способов. Для Django на хосте:

```bash
poetry run python manage.py loaddata habits/fixtures/initial_data.json
```

Для Docker Compose:

```bash
docker compose exec -T web python manage.py loaddata habits/fixtures/initial_data.json
```

Не используйте для этой загрузки `config.settings_ci`: там SQLite-база находится в памяти и исчезает после завершения процесса.

## Проверки и тесты

После `poetry install --with dev,lint` проверки можно выполнить локально без PostgreSQL и Redis, используя настройки CI. Команды запущены в подоболочке, чтобы тестовые переменные не остались в вашем терминале:

```bash
(
  set -e
  export DJANGO_SETTINGS_MODULE=config.settings_ci
  export SECRET_KEY=local-ci-key-not-for-production
  export DEBUG=True
  export CORS_ALLOW_ALL_ORIGINS=True

  poetry run python manage.py check
  poetry run python manage.py makemigrations --check --dry-run
  poetry run coverage run manage.py test --noinput
  poetry run coverage report -m
  poetry run flake8 .
)
```

`settings_ci` использует SQLite в памяти и eager-режим Celery; это настройки **только для проверок**, а не для обычного запуска или деплоя. Тесты создают собственные данные. Порог покрытия в workflow сейчас не задан: отчёт показывает результат, но сам по себе не блокирует снижение coverage.

## CI/CD и сервер

Workflow [Django CI](.github/workflows/ci.yml) запускается на каждый `push` и на `pull_request`:

- `lint` запускает Flake8; `checks` выполняет системную проверку и проверку миграций.
- `test` запускает тесты с coverage; `build` собирает Docker-образы после успешных линтера и тестов.
- `coverage` публикует отчёт для PR и обновляет данные бейджа при push в `main`. Для PR из fork комментарий может не публиковаться из-за ограничений прав токена.
- `check_server_status` и `deploy` запускаются только на push в `main`. Если `SERVER_IP` не задан, проверка завершается ошибкой; если порт 22 недоступен, deploy пропускается с предупреждением. Открытый порт сам по себе не подтверждает успешный вход или работоспособность приложения.

Бейдж coverage появится после первого успешного выполнения job `coverage` при push в `main`: action создаст отдельную ветку `python-coverage-comment-action-data`, в которую GitHub Actions должен иметь право записывать. PR в `develop` этого не делает.

### Настройка текущего деплоя

Для текущего workflow добавьте в **Settings → Secrets and variables → Actions**:

| Секрет | Назначение |
| --- | --- |
| `SERVER_IP` | Адрес сервера для проверки порта и SSH. |
| `SSH_USER` | Пользователь для подключения к серверу. |
| `SSH_KEY` | Приватный ключ выделенной deploy-учётной записи. |

Тесты используют временный `SECRET_KEY` из workflow; GitHub-секрет с таким именем им не нужен. Настоящий ключ Django должен находиться в `.env` на сервере. Если автоматический деплой не нужен, настройте или отключите соответствующие jobs до push в `main`.

Например, создайте отдельный ключ и установите его публичную часть для пользователя на сервере, заменив пример адреса:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
ssh-copy-id -i ~/.ssh/github_actions_deploy.pub deploy-user@203.0.113.10
```

Сохраните содержимое **приватного** ключа в GitHub Secret `SSH_KEY`, не добавляя его в репозиторий. Для неинтерактивного запуска ключ должен работать без запроса passphrase; ограничьте права deploy-пользователя и защитите ключ.

Под учётной записью `SSH_USER` установите Docker, Compose и Git. Например, на подготовленном тестовом сервере:

```bash
cd "/home/$USER"
git clone https://github.com/GrandBalaxon/Habits-Tracker.git Habits-Tracker
cd Habits-Tracker
[ -f .env ] || cp .env.template .env
# Заполните серверный .env, затем проверьте запуск:
docker compose up -d --build
docker compose ps -a
docker compose logs migrate
```

Workflow ожидает проект именно в `/home/$SSH_USER/Habits-Tracker`; пользователю нужен доступ к Docker и к `origin`. Он выполняет `git pull origin main`, останавливает контейнеры и пересобирает их, поэтому возможен простой. Если каталог уже существует, используйте его вместо повторного клонирования.
