from django.apps import AppConfig


class MobileSaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile_sale'


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
