<sub>Заполнениние README.md выполнено на GitHub с применением разметки [Markdown](https://docs.github.com/ru/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).</sub>

![Workflow status](https://github.com/awesky/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

__<details><summary>Описание</summary>__

Cайт Foodgram, «Продуктовый помощник».

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
</details>

__<details><summary>Технологии</summary>__

- [x] Python
- [x] Django
- [x] Django REST Framework
- [x] Nginx
- [x] Gunicorn
- [x] Docker
      
</details>

__<details><summary>Запуск проекта на удаленном сервере</summary>__

1. Клонируйте репозиторий ([официальная документация](https://docs.github.com/ru/repositories/creating-and-managing-repositories/cloning-a-repository))
    
2. Подключитесь к удаленному серверу

    <sub>_(пример для пользователя "customuser" и публичного IP-адреса сервера "84.201.161.196")_</sub>
    ```
    ssh customuser@84.201.161.196
    ```

3. Установите Docker ([официальная документация](https://docs.docker.com/engine/install/))

4. Задайте значения переменным в GitHub - Settings - (Secuity) Secrets and variables - Actions

    ```SECRET_KEY```      секретный ключ Django-проекта
    
    ```HOST```            публичный IP сервера
    
    ```USER```            имя пользователя на сервере
    
    ```SSH_KEY```         приватный ssh-ключ
    
    ```PASSPHRASE```      пароль ssh-ключа
    
    ```DOCKER_PASSWORD``` пароль от DockerHub
    
    ```DOCKER_USERNAME``` логин DockerHub
    
    ```DB_HOST```         db (установить указанное значение)

5. Запустите GitHub Workflow ([официальная документация](https://docs.github.com/ru/actions/using-workflows/manually-running-a-workflow))

6. Сервис будет доступен по адресу: [http://84.201.161.196/](http://84.201.161.196/)

    <sup>_(пример для сервера с публичным IP-адресом "84.201.161.196")_</sup>
    
7. Создайте суперпользователя для администрирования проекта на сервере
    
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```

8. Панель администратора доступна по адресу: [http://84.201.161.196/admin](http://84.201.161.196/admin)

    <sup>_(пример для сервера с публичным IP-адресом "84.201.161.196")_</sup>
    
9. (По желанию) загрузите подготовленную базу ингредиентов
    
    ```
    sudo docker-compose exec backend python manage.py load_ingredients
    ```
    
</details>

> ## Автор
> - [x] Made by awesky ([GitHub](https://github.com/awesky)) within [Yandex.Practicum](https://practicum.yandex.ru/) on August 2023.
