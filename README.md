### Pet-проект Foodgram

### Описание проекта 
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии:
Python:3.7

Django:3.2.18

DRF:3.12.4

Nginx:1.21.3

Gunicorn:20.1.0

PostgreSQL:13.0

### Как запустить проект

В файле директории ./infra/.env
Задайте имя пользователя и пароль для доступа к базе данных
В папке ./infra выполните команду

    $ docker compose up -d
    $ docker compose exec web python manage.py migrate
    $ docker compose exec web python manage.py collectstatic
    $ docker compose exec web python manage.py loaddata fixtures.json 

При выполнении этой команде сервис frontend, описанный в docker-compose.yml подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу. Проек запуститься в трёх контейнерах (nginx, PostgreSQL и Django), и будет доступен по адресу http://localhost

### Админ зона
Для доступа к админ зоне создайте суперпользователя
В папке ./infra выполните команду

    $ docker compose exec web python manage.py python manage.py createsuperuser

она будет доступна по http://localhost/admin/

### Документация
Увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/
В ней описаны возможные запросы к API
и структура ожидаемых ответов.