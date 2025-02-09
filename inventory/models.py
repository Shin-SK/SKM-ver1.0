from django.db import models

class InventoryItem(models.Model):
    product_name = models.CharField(max_length=200, verbose_name="商品名")
    stock_count = models.IntegerField(default=0, verbose_name="在庫数")
    product_code = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="商品コード")
    notes = models.TextField(blank=True, null=True, verbose_name="備考")
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True, verbose_name="商品画像")
    custom_fields = models.JSONField(default=list, blank=True, verbose_name="カスタムフィールド")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.product_name
