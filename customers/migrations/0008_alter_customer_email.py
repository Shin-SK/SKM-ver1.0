# Generated by Django 5.1.5 on 2025-02-25 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_alter_customer_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='メールアドレス'),
        ),
    ]
