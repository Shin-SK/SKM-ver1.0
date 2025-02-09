# Generated by Django 5.1.5 on 2025-01-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docspdf', '0005_invoice_closing_date_invoice_payment_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='quotationitem',
            name='subtotal',
            field=models.PositiveIntegerField(default=0, verbose_name='小計'),
        ),
        migrations.AlterField(
            model_name='quotationitem',
            name='unit_price',
            field=models.PositiveIntegerField(default=0, verbose_name='単価'),
        ),
    ]
