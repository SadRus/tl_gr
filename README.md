# tl_gr

### Table of content:
1. [Description](#description)
2. [Installing](#installing)
3. [Enviroment](#enviroment)
4. [Usage](#usage)
5. [API_Endpoint](#api_endpoint)
6. [Tests](#tests)

### Description 

Django app with telegram bot for fetching weather data from yandex weather api.

### Installing

1. Clone github repository:
```sh
git clone https://github.com/SadRus/tl_gr.git
```

2. Move to the project directory:
```sh
cd tl_gr/
```

3. Python3 must be [installed](https://www.python.org/).  
Check `python` is installed:
```sh
python --version
```

4. Create virtual enviroment (use python or python3):
```sh
python -m venv .venv
```

5. Activate virtual enviroment:  
- Windows: 
```
.\.venv\Scripts\activate
```  
- Linux: 
```sh
source .venv/bin/activate
```

6. Use `pip` (or `pip3`) for install requirements:
```sh
pip install -r requirements.txt
```  

7. Redis must be [installed](https://redis.io/docs/install/install-redis/).  
```sh
sudo apt-get update
sudo apt-get install redis
```  

8. Create .env file with enviroment variables (section below)  

9. Create default database and apply migrations:
```sh
python manage.py migrate
```

10. Parse cities from data file and create raws in db:
```sh
python parse_cities.py
```

### Enviroment

You needs to create .env file for the enviroment variables in main folder.

- `ALLOWED_HOSTS` - allowed hosts, while DEBUG=False
- `DEBUG` - debug mode (set False)
- `CACHE_TIMEOUT` - timeout(in minutes) for api requests
- `TG_BOT_TOKEN` - needs register the bot in telegram via https://t.me/BotFather
- `YANDEX_WEATHER_API_TOKEN` - token for fetching data from yandex api https://yandex.ru/dev/weather/  
- `SECRET_KEY` - django secret key (e.g. "django-insecure-0if40nf4nf93n4")
- `REDIS_HOST` - redis host's ip address (e.g. 'localhost')
- `REDIS_PORT` - redis port (default: 6379)

### Usage

1. Start django app from root directory:
```sh
python manage.py runserver
```

2. Open one more console and activate virtual enviroment:
- Windows: 
```
.\.venv\Scripts\activate
```  
- Linux: 
```sh
source .venv/bin/activate
```

3. Run telegram bot via django management command (while django app is running):
```sh
python manage.py runbot
```

4. Also, you can create the superuser for manually edit data from admin panel http://127.0.0.1:8000/admin/
```sh
python manage.py createsuperuser
```

### API_Endpoint

Example:
```
http://127.0.0.1:8000/api/weather?city=Калининград
```

### Tests

For running tests use console command:
```sh
python manage.py test
```