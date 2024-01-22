import requests

from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Weather
from .serializers import WeatherSerializer
from django.conf import settings


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
    return {
        'temperature': response_data['fact']['temp'],
        'pressure': response_data['fact']['pressure_mm'],
        'wind_speed': response_data['fact']['wind_speed'],
        'request_timestamp': response_data['now'],
    }


class WeatherAPIView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        weather = get_object_or_404(Weather, city=city)

        timestamp_now = datetime.now().timestamp()
        delta = timedelta(minutes=30).seconds
        timestamp_expired_at = weather.request_timestamp + delta

        if timestamp_now > timestamp_expired_at:
            weather_data = fetch_yandex_api_weather(weather)
            Weather.objects.filter(city=city).update(**weather_data)
            weather.refresh_from_db()

        serializer_class = WeatherSerializer(weather)
        return Response(serializer_class.data)
