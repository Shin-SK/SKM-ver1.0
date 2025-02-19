# accounts/adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class MyAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL  # "https"
        domain = settings.SITE_DOMAIN  # Heroku上のドメイン
        uid = emailconfirmation.key.split('-')[0]   # 実際の分解方法に合わせる
        token = emailconfirmation.key.split('-')[1]   # 実際の分解方法に合わせる
        return f"{protocol}://{domain}/activate/{uid}/{token}/"
