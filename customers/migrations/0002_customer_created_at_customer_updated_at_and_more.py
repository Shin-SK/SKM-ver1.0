# Generated by Django 5.1.5 on 2025-01-25 01:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='登録日時'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日時'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='会社名'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='名前（名）'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='名前（姓）'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='電話番号'),
        ),
    ]
