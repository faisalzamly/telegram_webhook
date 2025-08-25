from django.urls import path
from .views import telegram_webhook

urlpatterns = [
    path("<str:hook_secret>/webhook/", telegram_webhook, name="tg_webhook"),
]
