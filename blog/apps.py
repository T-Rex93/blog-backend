from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import requests

def ready(self):
    import blog.signals

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    send_to_monday(f"User Login: {user.username}", {"status": {"label": "Logged In"}})

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    send_to_monday(f"User Logout: {user.username}", {"status": {"label": "Logged Out"}})