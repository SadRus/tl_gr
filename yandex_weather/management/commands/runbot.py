from django.core.management.base import BaseCommand

from yandex_weather import tg_bot


class Command(BaseCommand):
    help = 'Run telegram bot'

    def handle(self, *args, **options):
        tg_bot.main()
