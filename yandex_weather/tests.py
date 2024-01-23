from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Weather


class WeatherModelTestCase(TestCase):
    def setUp(self):
        Weather.objects.create(
            city='Москва',
            latitude=55.75,
            longitude=37.62,
        )

    def test_unique_city_name(self):
        with self.assertRaises(IntegrityError):
            Weather.objects.create(
                city='Москва',
                latitude=55.75,
                longitude=37.62,
            )


class WeatherAPITestCase(APITestCase):
    def setUp(self):
        Weather.objects.create(
            city='Калининград',
            latitude=54.71,
            longitude=20.51,
        )

    def test_get(self):
        url = reverse('weather')
        response = self.client.get(url, {'city': 'Калининград'})
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['city'], 'Калининград')
