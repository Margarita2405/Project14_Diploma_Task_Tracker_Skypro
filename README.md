# 🚀 Task Tracker API

Бэкенд-сервис для управления задачами сотрудников. Реализован на Django REST Framework с JWT-аутентификацией,
полным CRUD, фильтрацией, пагинацией, документированным API (Swagger/ReDoc) и автоматическим деплоем через 
GitHub Actions.

---

## 📌 Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Локальный запуск](#локальный-запуск)
  - [С использованием Docker](#с-использованием-docker)
  - [Без Docker (ручной запуск)](#без-docker-ручной-запуск)
- [Переменные окружения](#переменные-окружения)
- [Тестирование](#тестирование)
- [Документация API](#документация-api)
- [CI/CD и деплой](#cicd-и-деплой)
- [Структура проекта](#структура-проекта)
- [Возможные проблемы и их решение](#возможные-проблемы-и-их-решение)
- [Автор](#автор)

---

## 🧩 Описание

Проект предоставляет REST API для трекинга задач. Пользователи могут:

- Регистрироваться и получать JWT-токены
- Создавать, просматривать, обновлять и удалять только свои задачи
- Фильтровать задачи по статусу, приоритету, ответственному
- Искать задачи по названию или описанию
- Получать задачи с пагинацией (10 записей на страницу)

Проект полностью контейнеризирован (Docker + docker-compose) и автоматически развёртывается на удалённом сервере
при пуше в ветку `develop`.

---

## 🛠 Технологии

- **Python 3.13**
- **Django 6.0.6** + **Django REST Framework 3.17.1**
- **JWT-аутентификация** (djangorestframework-simplejwt)
- **PostgreSQL 16** (в продакшене и в тестах)
- **Docker** / **docker-compose**
- **Nginx** (прокси‑сервер)
- **GitHub Actions** (CI/CD)
- **drf-yasg** (Swagger/ReDoc документация)
- **django-filter** (фильтрация)
- **gunicorn** (WSGI‑сервер)

---

## 🏁 Локальный запуск

### С использованием Docker (рекомендуется)

1. **Клонируйте репозиторий**
```
git clone https://github.com/Margarita2405/Project14_Diploma_Task_Tracker_Skypro
cd Project14_Diploma_Task_Tracker_Skypro
```

2. **Создайте файл .env (скопируйте .env.example и заполните)**

```
cp .env.example .env
```
Обязательно укажите SECRET_KEY, настройки базы данных и т.д.

3. **Запустите контейнеры**

```
docker-compose up --build
```
После запуска сервисы будут доступны:

API: http://localhost

Админка: http://localhost/admin

Swagger: http://localhost/swagger/

4. **Выполните миграции (в новом терминале)**

```
docker-compose exec web python manage.py migrate
```

5. **Создайте суперпользователя**

```
docker-compose exec web python manage.py createsuperuser
```

6. **Остановка**

```
docker-compose down
```

### Без Docker (ручной запуск)

1. **Создайте виртуальное окружение**

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

2. **Установите зависимости**

```
pip install -r requirements.txt
```

3. **Настройте базу данных (например, PostgreSQL или SQLite для разработки).
   Отредактируйте .env или напрямую settings.py.**

4. **Выполните миграции и создайте суперпользователя**

```
python manage.py migrate
python manage.py createsuperuser
```

5. **Запустите сервер разработки**

```
python manage.py runserver
```

API будет доступен по http://127.0.0.1:8000.

🔐 Переменные окружения (.env)

Создайте файл .env в корне проекта по образцу .env.example:

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Для Django (читаются в settings.py)
DATABASE_NAME=tasktracker
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

# Для образа PostgreSQL (используются контейнером db)
POSTGRES_DB=tasktracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

CORS_ALLOWED_ORIGINS=http://localhost
CSRF_TRUSTED_ORIGINS=http://localhost

DOCKER_HUB_USERNAME=your_dockerhub
DOCKER_HUB_ACCESS_TOKEN=your_token

SSH_USER=your_user_name
SERVER_IP=123.123.123.123
SSH_KEY=your_secret_key_here

Для продакшена установите DEBUG=False, добавьте реальный IP/домен в ALLOWED_HOSTS и используйте настоящие пароли.

🧪 Тестирование

Запуск всех тестов:

# Локально с Docker
```
docker-compose exec web python manage.py test
```

# Без Docker
```
python manage.py test
```

Для проверки покрытия (coverage):

```
coverage run manage.py test
coverage report -m
```

## Тесты включают:

- Регистрацию и аутентификацию

- CRUD операции с задачами

- Права доступа (пользователь видит/редактирует только свои задачи)

- Фильтрацию и поиск

- Пагинацию

📚 Документация API

Swagger UI: http://localhost/swagger/
ReDoc: http://localhost/redoc/

## Основные эндпоинты

Метод	    URL	                         Описание
POST	    /api/users/register/	     Регистрация пользователя
POST	    /api/token/	                 Получение JWT (access + refresh)
POST	    /api/token/refresh/	         Обновление access‑токена
GET	        /api/tasks/	                 Список задач (с фильтрацией)
POST	    /api/tasks/	                 Создание задачи
GET	        /api/tasks/{id}/	         Детали задачи
PUT/PATCH	/api/tasks/{id}/	         Обновление задачи
DELETE	    /api/tasks/{id}/	         Удаление задачи

## Фильтрация и поиск

- ?status=new / ?status=in_progress / ?status=completed

- ?priority=high / ?priority=medium / ?priority=low

- ?assigned_to=1

- ?search=текст (поиск по title и description)

- ?ordering=-created_at (сортировка)

## Пример запроса (создание задачи)

```
curl -X POST http://localhost/api/tasks/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Новая задача","priority":"high"}'
```

⚙️ CI/CD и деплой

Проект настроен на автоматический деплой через GitHub Actions при пуше в ветку develop.

## Процесс

1. Линтинг (flake8)
2. Тестирование (с PostgreSQL в контейнере)
3. Сборка Docker-образа (тег – хэш коммита)
4. Публикация образа в Docker Hub
5. Деплой на удалённый сервер по SSH:
- Клонирование/обновление репозитория
- Создание .env из GitHub Secrets
- Запуск docker-compose up -d
- Выполнение миграций

## Необходимые Secrets (настройки репозитория)

Secret	                    Описание
DOCKER_HUB_USERNAME	        Логин на Docker Hub
DOCKER_HUB_ACCESS_TOKEN	    Токен доступа к Docker Hub
SSH_KEY	                    Приватный SSH-ключ для доступа к серверу
SSH_USER	                Имя пользователя на сервере (например, test)
SERVER_IP	                Публичный IP адрес сервера
DJANGO_SECRET_KEY	        Секретный ключ Django
ADMIN_PASSWORD	            Пароль для суперпользователя (если нужно автоматическое создание)

## Ручной деплой (если не используется CI)

```
ssh test@<server_ip>
cd ~/tasktracker
git pull origin develop
docker-compose down
docker-compose up -d
docker-compose exec web python manage.py migrate
```

📁 Структура проекта

Project14_Diploma_Task_Tracker_Skypro/
├── .github/workflows/
│   └── ci.yml                # GitHub Actions pipeline
├── config/                   # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                   # Статические файлы (собираются)
├── media/                    # Медиафайлы (пусто)
├── tasks/                    # Приложение задач
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users/                    # Кастомная модель пользователя и регистрация
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .dockerignore                   
├── .env                      # Переменные окружения
├── .env.example              # Пример переменных окружения
├── .flake8
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── manage.py
└── README.md

⚠️ Возможные проблемы и их решение

## Ошибка relation "django_celery_beat_crontabschedule" does not exist

Проект не использует Celery, поэтому эта ошибка не должна возникать. Если появилась – проверьте, не остались ли
старые миграции от другого проекта. Убедитесь, что django_celery_beat не добавлен в INSTALLED_APPS.

## 502 Bad Gateway при обращении к сайту

- Проверьте, что контейнер web запущен: docker-compose ps

- Проверьте логи Nginx: docker-compose logs nginx

- Убедитесь, что в nginx.conf указан правильный proxy_pass http://web:8000;

## Не удаётся подключиться к базе данных

- Убедитесь, что в .env указан DATABASE_HOST=db (имя сервиса в docker-compose)

- Проверьте, что контейнер db здоров: docker-compose logs db

## Ошибка Permission denied при git pull на сервере

- Убедитесь, что SSH-ключ добавлен в GitHub (Settings → SSH and GPG keys)

- На сервере проверьте права на папку ~/tasktracker: chown -R test:test ~/tasktracker

👩‍💻 Автор

Маргарита Буршева

Email: mbursheva@mail.ru

Проект: https://github.com/Margarita2405/Project13_Course_work5_Skypro

Дипломный проект в рамках курса Skypro «Django REST Framework»
