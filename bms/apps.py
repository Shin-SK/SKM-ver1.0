from django.apps import AppConfig

class BmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bms'
    verbose_name = "社員情報"  # ← ここを変更！
