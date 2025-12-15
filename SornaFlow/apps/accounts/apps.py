from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Sets default primary key type for models
    name = 'apps.accounts'  # Full Python path of the app
    verbose_name = 'مدیریت اکانت ها'  # Human‑readable name shown in Django admin
