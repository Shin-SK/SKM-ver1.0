from django.db import models
from cloudinary.models import CloudinaryField  # Cloudinary対応

class CompanyProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name="会社名")
    logo = CloudinaryField(blank=True, null=True, verbose_name="会社ロゴ")
    seal = CloudinaryField(blank=True, null=True, verbose_name="会社印鑑")
    address = models.TextField(verbose_name="住所")
    phone = models.CharField(max_length=15, verbose_name="電話番号")
    email = models.EmailField(verbose_name="メールアドレス")
    contact_person = models.CharField(max_length=100, verbose_name="担当者名")
    bank_details = models.TextField(verbose_name="銀行口座", null=True, blank=True)

    class Meta:
        verbose_name = "会社情報"
        verbose_name_plural = "会社情報"

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo:
            url = self.logo.url
            if url.startswith("http://"):
                url = url.replace("http://", "https://", 1)
            return url
        return ""

    @property
    def seal_url(self):
        if self.seal:
            url = self.seal.url
            if url.startswith("http://"):
                url = url.replace("http://", "https://", 1)
            return url
        return ""
