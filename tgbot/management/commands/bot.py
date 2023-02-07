import logging
from django.core.management.base import BaseCommand
from loader import bot
from tgbot.handlers.client_handlers import register_handlers_client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


class Command(BaseCommand):
    help = "Запуск бота"

    def handle(self, *args, **kwargs):
        register_handlers_client()
        bot.run_polling()
