from .models import CompanyProfile

def get_sender_email():
    """会社情報のメールアドレスを送信元として取得"""
    company = CompanyProfile.objects.first()
    return company.email if company else "info@sk-tokyo.net"
