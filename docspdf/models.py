from django.db import models
from customers.models import Customer
from django.contrib.auth.models import User

class Quotation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客")
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="担当者名")
    attention_to = models.CharField(max_length=100, null=True, blank=True, verbose_name="宛先")
    quotation_number = models.CharField(max_length=20, unique=True, verbose_name="見積書番号")
    project_name = models.CharField(max_length=200, default="未設定", verbose_name="案件名")
    deadline = models.CharField(max_length=50, null=True, blank=True, verbose_name="納期")
    closing_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="締め日")
    payment_due_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="支払期日")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="制作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


    class Meta:
        verbose_name = "見積書"
        verbose_name_plural = "見積書一覧"

    def __str__(self):
        return f"{self.quotation_number} - {self.project_name} - {self.customer}"


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items", verbose_name="見積書")
    item_name = models.CharField(max_length=100, verbose_name="品名")
    quantity = models.PositiveIntegerField(verbose_name="数量", default=0)  # デフォルト値を追加
    unit_price = models.PositiveIntegerField(verbose_name="単価", default=0)  # デフォルト値を追加
    subtotal = models.PositiveIntegerField(verbose_name="小計", default=0)  # デフォルト値を追加

    class Meta:
        verbose_name = "見積項目"
        verbose_name_plural = "見積項目一覧"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price  # 小計を計算
        super().save(*args, **kwargs)



class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客")
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="担当者名")
    attention_to = models.CharField(max_length=100, null=True, blank=True, verbose_name="宛先")
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="請求書番号")
    project_name = models.CharField(max_length=200, default="未設定", verbose_name="案件名")  # 追加
    deadline = models.CharField(max_length=50, null=True, blank=True, verbose_name="納期")
    closing_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="締め日")
    payment_due_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="支払期日")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="制作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "請求書"
        verbose_name_plural = "請求書一覧"

    def __str__(self):
        return f"{self.invoice_number} - {self.project_name} - {self.customer}"



class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items", verbose_name="請求書")
    item_name = models.CharField(max_length=100, verbose_name="品名")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    unit_price = models.PositiveIntegerField(verbose_name="単価")
    subtotal = models.PositiveIntegerField(verbose_name="小計")

    class Meta:
        verbose_name = "請求項目"
        verbose_name_plural = "請求項目一覧"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
