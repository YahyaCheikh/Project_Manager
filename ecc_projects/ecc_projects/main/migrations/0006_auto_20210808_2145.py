# Generated by Django 3.1.13 on 2021-08-08 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210808_2137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['created_at']},
        ),
    ]