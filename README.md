# tl_gr

### Table of content:
1. [Description](#description)
2. [Installing](#installing)
3. [Enviroment](#enviroment)
4. [Usage](#usage)
5. [API_Endpoint](#api_endpoint)

### Description 

API and telegram bot for fetching weather data from yandex weather api.

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
- Windows: `.\.venv\Scripts\activate`  
- Linux: `source .venv/bin/activate`

6. Use `pip` (or `pip3`) for install requirements:
```sh
pip install -r requirements.txt
```  

7. Redis must be [installed](https://redis.io/docs/install/install-redis/).  
```sh
sudo apt-get update
sudo apt-get install redis
```  

### Enviroment

You needs to create .env file for the enviroment variables in main folder.

- `TG_BOT_TOKEN` - needs register the bot in telegram via https://t.me/BotFather
- `YANDEX_WEATHER_API_TOKEN` - token for fetching data from yandex api https://yandex.ru/dev/weather/  
- `DEBUG` - debug mode (set False)
- `SECRET_KEY` - django secret key (e.g. "django-insecure-0if40nf4nf93n4")
- `DATABASE_HOST` - redis host's ip address (e.g. 'localhost')
- `DATABASE_PORT` - redis port (default: 6379)

### Usage

First, start django app from root directory:
```python
python manage.py runserver
```

Second, run telegram bot via django management command:
```python
python manage.py runbot
```

### API_Endpoint

```
http://127.0.0.1:8000/weather?city=<city_name>
```