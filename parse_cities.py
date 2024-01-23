import os
import re

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from yandex_weather.models import Weather


def main():
    with open('cities.txt', 'r') as file:
        raw_cities = file.read().splitlines()

    cities = [re.split(' — |, ', city) for city in raw_cities if len(city) > 2]
    try:
        Weather.objects.bulk_create([
            Weather(
                city=city[0],
                latitude=city[1],
                longitude=city[2],
            ) for city in cities
        ])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
