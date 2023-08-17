<sub>Заполнениние README.md выполнено на GitHub с применением разметки [Markdown](https://docs.github.com/ru/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).</sub>

__<details><summary>Описание</summary>__
Cайт Foodgram, «Продуктовый помощник».
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
</details>

__<details><summary>Запуск проекта на удаленном сервере</summary>__
Подключитесь к удаленному серверу
```ssh customuser@84.201.161.196```
(пример для пользователя customuser и адреса сервера 84.201.161.196)

Установите Docker ([официальная документация](https://docs.docker.com/engine/install/))

Скопируйте необходимые файлы на сервер
```
scp docker-compose.yml nginx.conf customuser@84.201.161.196:/home/customuser/
```
(пример для пользователя customuser и адреса сервера 84.201.161.196)

Задайте значения переменным в GitHub - Settings - (Secuity) Secrets and variables - Actions
```
SECRET_KEY              - _секретный ключ Django-проекта_
```
```
HOST                    - _публичный IP сервера_
```
```
USER                    - _имя пользователя на сервере_
```
```
SSH_KEY                 - приватный ssh-ключ
```
```
PASSPHRASE              - _пароль ssh-ключа_
```
```
DOCKER_PASSWORD         - _пароль от DockerHub_
```
```
DOCKER_USERNAME         - _логин DockerHub_
```
```
DB_HOST                 - db
```

Запустите GitHub Workflow ([официальная документация](https://docs.github.com/ru/actions/using-workflows/manually-running-a-workflow))

Создайте суперпользователя для администрирования проекта на сервере
```sudo docker-compose exec backend python manage.py createsuperuser```

По желанию загрузите подготовленную базу ингредиентов
```sudo docker-compose exec backend python manage.py load_ingredients```
</details>

> ## Автор
> - [x] Made by awesky ([GitHub](https://github.com/awesky)) within [Yandex.Practicum](https://practicum.yandex.ru/) on August 2023.