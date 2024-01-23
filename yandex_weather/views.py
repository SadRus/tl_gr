import requests

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Weather
from .serializers import WeatherSerializer


def fetch_yandex_api_weather(weather):
    url = 'https://api.weather.yandex.ru/v2/forecast'
    yandex_token = settings.YANDEX_WEATHER_API_TOKEN

    headers = {'X-Yandex-API-Key': yandex_token}
    params = {
        'lang': 'ru_RU',
        'limit': 1,
        'hours': False,
        'extra': False,
        'lat': weather.latitude,
        'lon': weather.longitude,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response_data = response.json()
    print(response_data['now'])
    return {
        'temperature': response_data['fact']['temp'],
        'pressure': response_data['fact']['pressure_mm'],
        'wind_speed': response_data['fact']['wind_speed'],
    }


class WeatherAPIView(RetrieveAPIView):

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def get(self, request):
        city = request.query_params.get('city')
        weather = get_object_or_404(Weather, city=city)

        weather_data = fetch_yandex_api_weather(weather)
        Weather.objects.filter(city=city).update(**weather_data)
        weather.refresh_from_db()

        serializer_class = WeatherSerializer(weather)
        return Response(serializer_class.data)
