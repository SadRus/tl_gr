# Generated by Django 4.2 on 2024-01-23 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_weather', '0003_remove_weather_request_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='city',
            field=models.CharField(max_length=100, unique=True, verbose_name='Город'),
        ),
    ]
