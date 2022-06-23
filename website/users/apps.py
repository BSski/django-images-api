from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # def ready(self):
    #     from .models import UserTier
    #
    #     for tier in UserTier.objects.all():
    #         tier.save()
