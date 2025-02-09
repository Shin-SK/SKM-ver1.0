# Generated by Django 5.1.5 on 2025-01-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docspdf', '0004_invoice_invoiceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='closing_date',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='締め日'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_due_date',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='支払期日'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='closing_date',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='締め日'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='payment_due_date',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='支払期日'),
        ),
    ]
