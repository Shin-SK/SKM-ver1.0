# Generated by Django 5.1.5 on 2025-01-28 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0006_customfield_alter_employee_dynamic_attributes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomField',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='dynamic_attributes',
        ),
    ]
