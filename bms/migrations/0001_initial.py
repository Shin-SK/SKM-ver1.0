# Generated by Django 5.1.5 on 2025-01-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='名')),
                ('last_name', models.CharField(max_length=50, verbose_name='姓')),
                ('department', models.CharField(max_length=100, verbose_name='部署')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('phone_number', models.CharField(max_length=15, verbose_name='電話番号')),
            ],
        ),
    ]
