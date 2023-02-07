"""Клиентские клавиатуры"""
from telegram import ReplyKeyboardMarkup, KeyboardButton


keyboard = [
    [
        KeyboardButton("О нас"),
        KeyboardButton("Контакты"),
    ],
    [KeyboardButton("FAQ"), KeyboardButton("Как пользоваться?")],
]
reply_markup = ReplyKeyboardMarkup(keyboard)
