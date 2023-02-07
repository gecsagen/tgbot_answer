from django.db import models
from tgbot.services.string_comparison import string_comparison


class User(models.Model):
    """Пользователь тегерамм бота"""

    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(
        max_length=8, null=True, blank=True, help_text="Telegram client's lang"
    )
    deep_link = models.CharField(max_length=64, null=True, blank=True)

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"@{self.username}" if self.username is not None else f"{self.user_id}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Answer(models.Model):
    """Ответ на вопрос пользователя"""

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}_{self.text[:30]}"

    def comparison(self, user_question: str) -> float:
        """Возвращает средний процент похожести нескольких вопросов конкретного ответа"""
        questions = self.questions.values("text")
        result = [
            string_comparison(question["text"], user_question) for question in questions
        ]
        return max(result)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Question(models.Model):
    """Предполагаемые вопросы"""

    text = models.TextField(unique=True)
    answer = models.ForeignKey(
        Answer, related_name="questions", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}_{self.text[:30]}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Query(models.Model):
    """Запросы пользователя"""

    text = models.TextField(help_text="Запроса пользователя")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="queries", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id}_{self.text[:30]}"

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"


class QuestionFAQ(models.Model):
    """Вопрос для FAQ"""

    text = models.TextField(unique=True)

    def __str__(self):
        return f"{self.id}_{self.text[:30]}"

    class Meta:
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "Вопросы FAQ"


class AnswerFAQ(models.Model):
    """Ответ для FAQ"""

    text = models.TextField(unique=True)
    question_id = models.OneToOneField(
        QuestionFAQ, related_name="answer_faq", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id}_{self.text[:30]}"

    class Meta:
        verbose_name = "Ответ FAQ"
        verbose_name_plural = "Ответы FAQ"
