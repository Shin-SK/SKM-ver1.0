# Generated by Django 5.1.5 on 2025-01-27 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0004_employee_employee_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='dynamic_attributes',
            field=models.JSONField(blank=True, default=dict, verbose_name='動的属性'),
        ),
    ]
