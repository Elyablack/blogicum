# Blogicum

Blogicum - это проект на Django, который предоставляет пользователям возможность создавать, редактировать и комментировать посты на различные темы. Пользователи могут прикреплять изображения с местоположением и просматривать свой личный кабинет с возможностью управления постами и комментариями. Администрация имеет доступ к панели управления, где можно управлять всеми постами и комментариями.

## Функциональные возможности

### Создание и редактирование постов
Все зарегистрированные пользователи могут:
- Создавать посты с добавлением изображений.
- Указывать местоположение и категорию поста.
- Устанавливать дату публикации поста самостоятельно.

Незарегистрированные пользователи могут просматривать посты и комментарии, но не могут комментировать и редактировать посты.

### Комментарии
Все зарегистрированные пользователи могут оставлять комментарии к постам.

### Личный кабинет
Все зарегистрированные пользователи могут:
- Просматривать и редактировать свой профиль.
- Управлять своими постами и комментариями.

### Панель администратора
Администраторы имеют следующие возможности через Django Admin:
- Управление всеми постами и комментариями (удаление, редактирование, создание новых).
- Управление правами пользователей (наделение и ограничение прав, удаление, редактирование, создание новых пользователей).

### Авторизация и аутентификация
Все действия на сайте защищены системой авторизации и аутентификации. Доступ к функциям и страницам регулируется в зависимости от прав пользователя.

## Стек технологий

![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=python&logoColor=56C0C0&color=008080)
![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)
![HTML5](https://img.shields.io/badge/-HTML5-464646?style=flat&logo=html5&logoColor=56C0C0&color=008080)
![CSS3](https://img.shields.io/badge/-CSS3-464646?style=flat&logo=css3&logoColor=56C0C0&color=008080)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-464646?style=flat&logo=bootstrap&logoColor=56C0C0&color=008080)
![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat&logo=sqlite&logoColor=56C0C0&color=008080)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)
![Pillow](https://img.shields.io/badge/-Pillow-464646?style=flat&logo=pillow&logoColor=56C0C0&color=008080)
![Geopandas](https://img.shields.io/badge/-Geopandas-464646?style=flat&logo=geopandas&logoColor=56C0C0&color=008080)

## Установка

1. Склонируйте репозиторий на свой компьютер:
    ```
    git@github.com:Elyablack/django_sprint4.git
    ```
2. Создайте и активируйте виртуальное окружение:
   ```
   python3 -m venv venv
   source venv/bin/activate
    ```
3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
4. Миграция базы данных:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Создание суперпользователя:
    ```
    python manage.py createsuperuser
    ```
6. Запуск сервера разработки:
    ```
    python manage.py runserver
    ```
### Автор
[Elvira Ahmedyanova - Elyablack](https://github.com/Elyablack)
