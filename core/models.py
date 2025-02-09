from django.db import models

class CompanyProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name="会社名")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="会社ロゴ")
    seal = models.ImageField(upload_to='seals/', null=True, blank=True, verbose_name="会社印鑑")  # 追加
    address = models.TextField(verbose_name="住所")
    phone = models.CharField(max_length=15, verbose_name="電話番号")
    email = models.EmailField(verbose_name="メールアドレス")
    contact_person = models.CharField(max_length=100, verbose_name="担当者名")
    bank_details = models.TextField(verbose_name="銀行口座", null=True, blank=True)  # ← 追加

    class Meta:
        verbose_name = "会社情報"
        verbose_name_plural = "会社情報"

    def __str__(self):
        return self.name
