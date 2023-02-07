##  About the project:  
The project implements a telegram bot with an admin panel on Django. The bot can answer the user's questions. The bot administrator can ask DB questions regarding low and answers, the bot compares users' questions with questions from the DB and selects the most relevant answer. The bot does not compare blindly, but by percentage of probability, and thus gives the most relevant answer.

## Stack:
1. Bot: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot")
2. Web-admin: [Django](https://www.djangoproject.com/ "Django")

## Local launch:  
1. Clone the repository:  
`git clone https://github.com/gecsagen/tgbot_answer`  
2. Creating a virtual environment:  
```
bot_answer
pyhon -m venv .venv
```
3. Activate the environment:  
`source .venv/bin/activate`  
4. Installing dependencies:  
`pip install -r requirements.txt`  
5. Create a **settings.json** file at the root of the project and fill in the required settings. The project has an example file named **settings.examle.json**:  
```
"token": "Telegram bot token"
"about_as": "Company Information"
"contact_phones": "List of phones"
"contact_emails": "List of emails"
"address_list": "Address list"
"how_to_use": "Information on how to use the bot
"debug": "Debug mode for Django
"secret_key": "Django project secret key"

```
Follow the pattern from **settings.examle.json**  

7. Performing migrations:  
`python manage.py migrate`  
6. Create an admin user:  
`python manage.py createsuperuser`  
8. We launch the admin panel:  
`python manage.py runserver`  
or through **gunicorn**:  
`gunicorn --bind 0.0.0.0:8000 config.wsgi`  
9. Go to the admin panel at **127.0.0.1:8000** and fill in the admin panel with questions and answers.  
10.Run the bot in a separate terminal:  
`python manage.py bot`  
## Deploy:  
1. Clone the repository:  
`git clone https://github.com/gecsagen/tgbot_answer`  
2. Run the script **setup.sh**   
`./setup.sh`  
3. Create a **settings.json** file at the root of the project and fill in the required settings. The project has an example file named **settings.examle.json**  
4. Create an admin user:  
`python manage.py createsuperuser`  
5.Create file **systemd**:  
`sudo nano /etc/systemd/system/gunicorn.socket`  
With the following content:  
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
5. Create a service file **systemd** for **gunicorn** with the following command:

`sudo nano /etc/systemd/system/gunicorn.service`  

**Note:**  
❗it is assumed that you clone the project to the **root** directory, so all paths in the configs are configured in this way. If you clone the project to another directory, then change the paths in the configs to valid ones❗
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
6. Start the **systemd gunicorn** service from the previous step:
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```  
7. Create **nginx** config:   
`sudo nano /etc/nginx/sites-available/tgbot_answer`  
With the following content:  
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
❗Be sure to change ip server_name **93.202.86.15** to the ip of your server❗ 
8. Change user **nginx**:   
`sudo nano /etc/nginx/nginx.conf`  
Change the user in the first line to **root**:    
`user root;`  
9. Associate the file with the site support directory:  
`sudo ln -s /etc/nginx/sites-available/tgbot_answer /etc/nginx/sites-enabled`  
10. Restart nginx, allow the port in the firewall:  
```
systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo systemctl status nginx
``` 
11. Create a bot start service:  
`sudo nano /etc/systemd/system/bot.service`  
With the following content:    
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
12. Start the bot service:  
```
systemctl start bot.service
systemctl enable bot.service
systemctl status bot
```

13. Now go to http://domain_name_or_server_ip/admin and you will be taken to the bot's admin panel. You must enter your username and password. Then you can fill the database with questions and answers.




