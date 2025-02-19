# accounts/adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class MyAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
        domain = settings.SITE_DOMAIN  # settingsで定義したドメイン
        uid = emailconfirmation.key.split('-')[0]  # ※ここは適宜変更
        token = emailconfirmation.key.split('-')[1]  # ※ここは適宜変更
        # ※実際のキーの分解方法は、利用している実装に合わせてください
        return f"{protocol}://{domain}/activate/{uid}/{token}/"
