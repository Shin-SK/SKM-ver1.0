# Generated by Django 5.1.5 on 2025-01-30 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventoryitem_custom_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='custom_fields',
            field=models.JSONField(blank=True, default=list, verbose_name='カスタムフィールド'),
        ),
    ]
