# Generated by Django 3.1.13 on 2021-08-14 13:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_entreprisemodel_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodel',
            name='members',
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='developers',
            field=models.ManyToManyField(related_name='projectdev', to='main.PersonModel', verbose_name='Developers'),
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.personmodel'),
        ),
        migrations.AddField(
            model_name='projectmodel',
            name='validators',
            field=models.ManyToManyField(related_name='projectvalid', to='main.PersonModel', verbose_name='Validators'),
        ),
        migrations.AddField(
            model_name='task',
            name='total_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='role',
            field=models.CharField(choices=[('Entreprener', 'Entreprener'), ('Developer', 'Developer'), ('Validator', 'Validator')], max_length=255, verbose_name='Role'),
        ),
    ]
