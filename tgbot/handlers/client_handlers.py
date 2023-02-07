"""Клиентские хендлеры"""
import asyncio
from loader import bot
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from tgbot.keyboards import client_keyboards
from tgbot.settings.config import (
    about_as,
    how_to_use,
    address_list,
    contact_emails,
    contact_phones,
)
from tgbot.services.db import (
    sql_add_user,
    sql_get_questions,
    get_the_most_relevant_answer,
    add_query_of_user,
    get_all_admins,
)
from tgbot.models import Answer
from asgiref.sync import sync_to_async
from tgbot.settings import constants
from django.db.utils import IntegrityError


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для команды start"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=how_to_use,
    )
    await update.message.reply_text(
        constants.MENU, reply_markup=client_keyboards.reply_markup
    )
    try:
        #  пробуем добавить пользователя в БД
        await sql_add_user(update)
    except IntegrityError:
        pass


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для команды about"""
    await update.message.reply_html(about_as)


async def contants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для команды контакты"""
    if address_list:
        await update.message.reply_html(constants.OUR_ADDRESS)
        for x in address_list:
            address = x.get("address")
            latitude, longitude = x.get("coordinates")
            await update.message.reply_text(address)
            await update.message.reply_location(latitude, longitude)
        await update.message.reply_html(
            constants.OUR_PHONES + "\n".join(contact_phones)
        )
        await update.message.reply_html(
            constants.OUR_EMAILS + "\n".join(contact_emails)
        )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для команды faq"""
    #  получаем список вопрос - ответ для FAQ
    questions_answers = await sync_to_async(sql_get_questions)()
    for question, answer in questions_answers:
        await update.message.reply_html(question)
        await update.message.reply_text(answer)
        await asyncio.sleep(0.3)


async def how_to_use_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для команды how_to_use"""
    await update.message.reply_text(how_to_use)


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Хендлер для вопроса от юзера"""
    #  получаем наиболее релевантный ответ на вопрос юзера
    answer_id, grade = await sync_to_async(get_the_most_relevant_answer)(update)
    if grade > 0.4:
        answer = await Answer.objects.aget(pk=answer_id)
        await update.message.reply_text(answer.text)
    else:
        await update.message.reply_text(constants.CAN_NOT_ANSWER)
        #  отправляем админам сообщение, на которое не смог ответить бот
        list_users_id = await sync_to_async(get_all_admins)()
        for user_id in list_users_id:
            await context.bot.send_message(
                chat_id=f"{user_id}",
                text=constants.MESSAGE_ADMIN.format(
                    update.message.from_user.username, update.message.text
                ),
            )
    # записывает запрос пользоваетеля в БД
    await sync_to_async(add_query_of_user)(update)


def register_handlers_client():
    """
    Функция регистратор клиентских
    диспетчеров, вызывается из main.py
    """

    start_handler = CommandHandler("start", start)
    bot.add_handler(start_handler)
    about_handler = MessageHandler(
        filters.Text(
            "О нас",
        ),
        about,
    )
    bot.add_handler(about_handler)
    contants_handler = MessageHandler(
        filters.Text(
            "Контакты",
        ),
        contants,
    )
    bot.add_handler(contants_handler)
    faq_handler = MessageHandler(
        filters.Text(
            "FAQ",
        ),
        faq,
    )
    bot.add_handler(faq_handler)
    how_to_use_bot_handler = MessageHandler(
        filters.Text(
            "Как пользоваться?",
        ),
        how_to_use_bot,
    )
    bot.add_handler(how_to_use_bot_handler)
    question_handler = MessageHandler(filters.Text(), question)
    bot.add_handler(question_handler)
