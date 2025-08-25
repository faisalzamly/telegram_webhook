from django.db import models

class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.chat_id}"

class TgMessage(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    raw = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg to {self.user} at {self.created_at:%Y-%m-%d %H:%M}"
