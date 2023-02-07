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
5. Создайте файл **settings.json** в корне проекта и заполните необходимые настройки. В проекте есть пример файла с именем **settings.examle.json**:  
```
"token": "  Токен телеграм бота"
"about_as": "Информация о компании"
"contact_phones": "Список телефонов"
"contact_emails": "Список емайлов"
"address_list": "Список адресов"
"how_to_use": "Информация как пользоваться ботом
"debug": "Режим отладки для Django
"secret_key": "Секретный ключ проекта Django"  

```
Следуйте образцу из **settings.examle.json**  

7. Выполняем миграции:  
`python manage.py migrate`  
6. Создаем пользователя админки:  
`python manage.py createsuperuser`  
8. Запускаем админку:  
`python manage.py runserver`  
или через **gunicorn**:  
`gunicorn --bind 0.0.0.0:8000 config.wsgi`  
9. Переходим в админку по **127.0.0.1:8000** и заполняем вопросами ответами админку.  
10. Запускаем бота в отдельном терминале:  
`python manage.py bot`  
## Деплой:  
1. Клонируем репозиторий:  
`git clone https://github.com/gecsagen/tgbot_answer`  
2. Запускаем скрипт **setup.sh**  
`./setup.sh`  
3. Создайте файл **settings.json** в корне проекта и заполните необходимые настройки. В проекте есть пример файла с именем **settings.examle.json**  
4. Создаем пользователя админки:  
`python manage.py createsuperuser`  
5. Создаем файл **systemd**:  
`sudo nano /etc/systemd/system/gunicorn.socket`  
Со следующим содержанием:  
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
5. Cоздаем служебный файл **systemd** для **gunicorn** с помощью следующей команды:  

`sudo nano /etc/systemd/system/gunicorn.service`  

Примечание:  
предполагается что вы склонируете проект в директорию **root**, поэтому все пути в конфигах настроенны таким образом. Если вы склоируете проект в другую директорию, то измените пути в конфигах на валидные.
```  
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/tgbot_answer
ExecStart=/root/tgbot_answer/.venv/bin/gunicorn \
        --access-logfile - \
        --workers 3 \
        --bind unix:/run/gunicorn.sock \
        config.wsgi:application
        
[Install]
WantedBy=multi-user.target
```
6. Запускаем сервис **systemd gunicorn** из предыдущего шага:  
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```  
7. Создайте конфиг **nginx**:  
`sudo nano /etc/nginx/sites-available/tgbot_answer`  
Со следующим содержимым:  
```
server {
    listen 80;
    server_name 93.202.86.15;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    location  /static/ {
        root /root/tgbot_answer;
    }
}
```
🔴❗Обязательно поменяйте ip server_name **93.202.86.15** на ip вашего сервера❗🔴    
8. Измените пользователя **nginx**: 
`sudo nano /etc/nginx/nginx.conf`  
Измените пользователя в первой строчке на **root**:  
`user root;`  
9. Свяжите файл с каталогом поддержки сайтов:  
`sudo ln -s /etc/nginx/sites-available/tgbot_answer /etc/nginx/sites-enabled`  
10. Перезапустите nginx, разрешите порт в фаеволе:  
```
systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo systemctl status nginx
``` 
11. Создайте сервис запуска бота:  
`sudo nano /etc/systemd/system/bot.service`  
Со следующим содержимым:  
```
[Unit]
Description=bot daemon
Requires=gunicorn.service
After=gunicorn.service

[Service]
User=root
Group=www-data
WorkingDirectory=/root/tgbot_answer
ExecStart=/root/tgbot_answer/bot.sh

[Install]
WantedBy=multi-user.target
```  
12. Запустите сервис бота:  
```
systemctl start bot.service
systemctl enable bot.service
systemctl status bot
```

13. Теперь перейдите по **http://domain_name_or_server_IP/admin** и вы попадете в админку бота. Необходимо ввести логин и пароль. 





