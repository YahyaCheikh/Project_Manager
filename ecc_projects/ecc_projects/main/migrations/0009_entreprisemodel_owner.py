# Generated by Django 3.1.13 on 2021-08-12 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210812_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreprisemodel',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.personmodel', verbose_name='Owner'),
        ),
    ]
