# Generated by Django 5.1.5 on 2025-01-31 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_companyprofile_bank_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='closing_date',
        ),
        migrations.RemoveField(
            model_name='companyprofile',
            name='payment_due_date',
        ),
    ]
