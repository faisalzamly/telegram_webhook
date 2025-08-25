from django.contrib import admin
from .models import TgUser, TgMessage

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "username", "created_at")
    search_fields = ("chat_id", "username")

@admin.register(TgMessage)
class TgMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__chat_id", "text")
