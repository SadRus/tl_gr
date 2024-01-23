from django.db import models


class Weather(models.Model):
    city = models.CharField(
        'Город',
        max_length=100,
        unique=True
    )
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    temperature = models.FloatField(
        'Текущая температура',
        blank=True,
        null=True,
    )
    pressure = models.FloatField(
        'Давление в мм рт.ст.',
        blank=True,
        null=True,
    )
    wind_speed = models.FloatField(
        'Скорость ветра',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.city
