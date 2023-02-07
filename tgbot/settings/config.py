"""Файл конфигурации для загрузки значений из переменного окружения"""
import json
from dataclasses import dataclass


@dataclass
class Settings:
    token: str
    about_as: str
    contact_phones: list
    contact_emails: list
    address_list: list[dict]
    how_to_use: str
    debug: bool
    secret_key: str
    


def get_settings():
    """Возвращает провалидированые настройки бота"""
    with open("settings.json", "r", encoding="utf-8") as file_settings:
        return Settings(**json.load(file_settings))


settings = get_settings()
token = settings.token
about_as = settings.about_as
contact_phones = settings.contact_phones
contact_emails = settings.contact_emails
address_list = settings.address_list
how_to_use = settings.how_to_use
debug = settings.debug
secret_key = settings.secret_key