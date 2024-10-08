# Фудграм
«Фудграм» — сайтом, на котором пользователи будут публиковать рецепты, 
добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Пользователям сайта также будет доступен сервис «Список покупок». 
Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Стэк технологий
    - Python 3.9
    - Django REST Framework 3.14
    - Django 3.2
    - djoser 2.1.0
    - PostgreSQL 13.12
    - gunicorn 20.1.0
    - CI/CD GitHub Actions

## Как установить
1. Форкните и клонируйте проект в удобное место:\
   `cd нужное_место`\
   `git clone ссылка_на_git`
2. Создать файл .evn в корневой дериктории проекта:\
   `cp -n .env.expamle .env`\
   Описание переменных в .env.expamle: \
   `cat .env.expamle`
3. Указать в GitHub секреты Actions secrets:
   ```
   DOCKER_PASSWORD='Пароль от докер хаба'
   DOCKER_USERNAME='Пользователь докерхаба'
   HOST='адрес удаленного сервера'
   USER='пользователь на удаленном сервере'
   SSH_KEY='закрытый ключ доступа к серверу'
   SSH_PASSPHRASE='пароль от закрытого ключа'
   TELEGRAM_TO='ид учетки телеграмма'
   TELEGRAM_TOKEN='Токен бота'
   ```
4. Запушить для деплоя\
   `git push`
5. Применить миграции\
   `cd infra/`
   `make migrate`
6. Наполнить бд\
   `make add_db` 
7. Создать СуперПользователя\
   `make su`

## Проект доступен по адресу
   `http://158.160.64.213/` 

## Документаци API доступна по адресу
   `http://158.160.64.213/api/docs/`

## Об авторе
Андрей Тетнёв  
[GitHub](https://github.com/AndrewDevMan/) | [E-mail](mailto:andreytetnev@yandex.ru)
