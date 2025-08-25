import os, json, requests
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import TgUser, TgMessage

HOOK_SECRET = os.environ.get("TG_HOOK_SECRET")  # قيمة سرية لمسار الويبهوك
BOT_TOKEN   = os.environ.get("BOT_TOKEN")       # توكن البوت من BotFather

def send_message(chat_id, text):
    if not BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@csrf_exempt
def telegram_webhook(request, hook_secret):
    # تحقق من السر
    if hook_secret != HOOK_SECRET:
        return HttpResponseForbidden("Forbidden")

    if request.method != "POST":
        return JsonResponse({"ok": True, "message": "Use POST"})

    payload = json.loads(request.body.decode("utf-8"))
    msg = payload.get("message") or payload.get("edited_message") or {}
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    text = msg.get("text") or ""

    if chat_id:
        user, _ = TgUser.objects.get_or_create(
            chat_id=chat_id,
            defaults={"username": (msg.get("from") or {}).get("username")}
        )
        TgMessage.objects.create(user=user, text=text, raw=payload)

        reply = f"تم الاستلام ✅: {text[:200]}" if text else "تم الاستلام ✅"
        send_message(chat_id, reply)

    return JsonResponse({"ok": True})
