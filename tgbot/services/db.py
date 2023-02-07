"""Модуль для работы с БД бота"""
from telegram import Update
from tgbot.models import User, Answer, QuestionFAQ, Query


async def sql_add_user(update: Update) -> None:
    """Создание нового пользователя"""
    await User.objects.acreate(
        user_id=update.message.from_user.id,
        username=update.message.from_user.username,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
        language_code=update.message.from_user.language_code,
    )


def sql_get_questions():
    """Получение списка вопросов"""
    return [(x.text, x.answer_faq.text) for x in QuestionFAQ.objects.all()]


def get_the_most_relevant_answer(update: Update) -> tuple:
    """Возвращает наиболее релевантный ответ на запрос пользователя"""
    results = [
        (answer.id, answer.comparison(update.message.text))
        for answer in Answer.objects.all()
    ]
    return max(results, key=lambda i: i[1])

def get_all_admins():
    """Возвращает список id всех администраторов"""
    return [str(x.user_id) for x in User.objects.filter(is_admin=True)]


def add_query_of_user(update: Update):
    """Добавляет запрос пользователя в историю"""
    #  получаем пользователя
    user = User.objects.get(user_id=update.message.from_user.id)
    Query.objects.create(text=update.message.text, user=user)