from django.contrib import admin

from .models import User, Answer, Question, Query, QuestionFAQ, AnswerFAQ


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "is_banned",
        "is_admin",
        "is_moderator",
        "created_at",
    )
    list_filter = ("is_banned", "is_admin", "is_moderator", "created_at")
    list_editable = ("is_banned", "is_banned", "is_admin", "is_moderator")
    list_display_links = ("user_id",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    list_display_links = ("id", "text", "created_at", "updated_at")
    search_fields = ("text",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "updated_at", "answer")
    list_filter = ("created_at", "updated_at")
    list_display_links = ("id", "text", "created_at", "updated_at")
    search_fields = ("text",)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "user")
    list_filter = ("user", "created_at")
    search_fields = ("text",)


@admin.register(QuestionFAQ)
class QuestionFAQAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)


@admin.register(AnswerFAQ)
class AnswerFAQAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)
