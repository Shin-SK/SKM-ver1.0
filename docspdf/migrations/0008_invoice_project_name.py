# Generated by Django 5.1.5 on 2025-02-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docspdf', '0007_quotation_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='project_name',
            field=models.CharField(default='未設定', max_length=200, verbose_name='案件名'),
        ),
    ]
