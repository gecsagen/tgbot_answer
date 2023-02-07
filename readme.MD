##  О проекте:  
Проект реализует телеграм бота с админкой на Django. Бот может отвечать на вопросы пользователя. Администратор бота может заполнить БД любым количеством вопросов и ответов, бот сравнивает вопрос пользователя с вопросами из БД и выбирает наиболее релевантный ответ. Бот сравнивает не слепо, а по процентам похожести и т.о выдает наиболее релевантный ответ.  

## Стек:
1. Бот: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot")
2. Админка: [Django](https://www.djangoproject.com/ "Django")

## Локальный запуск:  
1. Клонируем репозиторий:  
`git clone https://github.com/gecsagen/tgbot_answer`  
2. Создаем виртуальное окружение:  
```
bot_answer
pyhon -m venv .venv
```
3. Активируем окружение:  
`source .venv/bin/activate`  
4. Устанавливаем зависимости:  
`pip install -r requirements.txt`  
5. Выполняем миграции:  
`python manage.py migrate`  
6. Создаем пользователя админки:  
`python manage.py createsuperuser`  
8. Запускаем админку:  
`python manage.py runserver`  
или через gunicorn:  
`gunicorn --bind 0.0.0.0:8000 config.wsgi`  
9. Переходим в админку по 127.0.0.1:8000 и заполняем вопросами ответами админку.  
10. Запускаем бота в отдельном терминале:  
`python manage.py bot`  


