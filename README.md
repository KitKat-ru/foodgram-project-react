## Foodgram
### Описание: ###

Дипломный проект Foodgram (Web, REST API) онлайн-сервис для публикации кулинарных рецептов на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, который в поседствии можно будет скачать и отправится в магазин для покупки необходимых ингредиентов.

Реализован на 3 docer-контейнерах: Django+Gunicorn, Nginx, PostgreSQL. Стек технологий - Python3.9, Django2.2, Docker, Gunicorn, Nginx, PostgreSQL. Размещен на удаленном сервере (Яндекс Облако, ОС Ubuntu 20.04). Реализована аутентификация на библиотеке `Djoser` и дефольной библиотеке `rest_framework.authtoken`.

## Установка: ##

### Клонируйте репозиторий: ###

    git clone git@github.com:KitKat-ru/foodgram-project-react.git


### Пример файла `.env`. Должен находится в папке `./foodgram-project-react/infra/`: ###
### Такие же `Secrets` должны быть созданы в `GitHub Actions`: ###

    DOCKER_USERNAME=... (имя пользователя (не логин) на DockerHub)
    LOGIN_DOCKER=... (логин пользователя на DockerHub)
    PASSWORD_DOCKER=... (пароль пользователя на DockerHub)

    SSH_KEY=... (ssh ключ указанный для ВМ)
    PASSPHRASE=... (пароль на ssh ключе)
    HOST=... (IP ВМ)
    USER=... (логин в ВМ)

    TELEGRAM_TO=... (ID чата в телеграмме)
    TELEGRAM_TOKEN=... (TOKEN бота в телеграмме)

    SECRET_KEY=... (ключ к Джанго проекту)
    DB_ENGINE=django.db.backends.postgresql (указываем, что работаем с postgresql)
    DB_NAME=postgres (имя базы данных)
    POSTGRES_USER=... (логин для подключения к базе данных)
    POSTGRES_PASSWORD=... (пароль для подключения к БД (установите свой)
    DB_HOST=db (название сервиса (контейнера)
    DB_PORT=5432 (порт для подключения к БД)
    DOMAIN=... (указать домен на котором будет находится сайт)
    SSL_CERT_EMAIL=... (почта для регистрации сертификата SSL)

### Скопируйте файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно ###

  
### Подготовьте ВМ. Остановите службу nginx. Установите - [Docker и Docker-compose](https://docs.docker.com/engine/install/ubuntu/): ###

    sudo apt update
    sudo apt upgrade
    sudo systemctl stop nginx
    sudo apt install docker.io

### При использовании команды `git push` запуститься `GitHub Actions` и задеплоит проект на вашу ВМ: ###
    git add .
    git commit -m 'you_text'
    git push

### После развертывания проекта заходите в ВМ и создайте миграции и заполнените базу данных: ###

    sudo docker-compose exec backend python manage.py migrate
    sudo docker-compose exec backend python manage.py createsuperuser
    sudo docker-compose exec backend python manage.py collectstatic --no-input

## Алгоритм регистрации и авторизации пользователей ##
  
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email`, `username`, `first_name`, `last_name`, `password` на эндпоинт `/api/users/`.
2. Пользователь отправляет POST-запрос с параметрами `email` и `password` на эндпоинт `/api/auth/token/login/`, в ответе на запрос ему приходит token (auth_token).  
5. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/users/me/` и заполняет поля в своём профайле.

### Для тестирования REST API можно обратиться по `URL`:
    https://food-ts.ddns.net/api/
    
### Для тестирования Web-сервиса можно обратиться по `URL`:    
    
    https://food-ts.ddns.net/recipes/

### панель администратора единая, доступна по `URL`:

    https://food-ts.ddns.net/admin/

### Автор:

- #### [Фабриков Артем](https://github.com/KitKat-ru)

### Лицензия:
- Этот проект лицензируется в соответствии с лицензией MIT ![](https://miro.medium.com/max/156/1*A0rVKDO9tEFamc-Gqt7oEA.png "1")

## Образ выложен на DockerHub, что бы его скачать введите:

    sudo docker pull taeray/backend:v1.1


## Плашка о прохождении `workflow`:
![example workflow](https://github.com/KitKat-ru/foodgram-project-react/actions/workflows/main.yml/badge.svg)
