from django.core.management.base import BaseCommand
import os, requests

class Command(BaseCommand):
    help = "Set Telegram webhook to your public URL"

    def add_arguments(self, parser):
        parser.add_argument("--url", required=False, help="Public base URL, e.g. https://abc.ngrok-free.app")

    def handle(self, *args, **opts):
        token  = os.environ.get("BOT_TOKEN")
        secret = os.environ.get("TG_HOOK_SECRET")
        base   = opts.get("url") or os.environ.get("PUBLIC_URL")

        if not token or not secret or not base:
            self.stderr.write("Need BOT_TOKEN, TG_HOOK_SECRET and PUBLIC_URL (or --url)")
            return

        hook_url = f"{base.rstrip('/')}/tg/{secret}/webhook/"
        r = requests.get(
            f"https://api.telegram.org/bot{token}/setWebhook",
            params={"url": hook_url}
        )
        self.stdout.write(f"setWebhook -> {r.status_code}: {r.text}\nURL: {hook_url}")
