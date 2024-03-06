from django.apps import AppConfig
import pretty_errors


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game"
