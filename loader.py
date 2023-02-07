"""Создается объект бота"""
from telegram.ext import ApplicationBuilder
from tgbot.settings.config import token

bot = ApplicationBuilder().token(token).build()