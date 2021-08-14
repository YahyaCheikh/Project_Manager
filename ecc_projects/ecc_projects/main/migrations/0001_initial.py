# Generated by Django 3.1.13 on 2021-07-27 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_assigned', models.BooleanField(default=False)),
                ('estimated_durattion', models.DurationField()),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('estimated_end_time', models.DateTimeField(blank=True, null=True)),
                ('time_left', models.DurationField(blank=True, null=True)),
                ('is_finich_at_time', models.BooleanField(blank=True, null=True)),
                ('difuculty_level', models.CharField(choices=[('VE', 'Very Easy'), ('E', 'Easy'), ('M', 'Medum'), ('H', 'Hard'), ('VH', 'Very Hard')], max_length=2)),
                ('status', models.CharField(choices=[('CR', 'Created'), ('AS', 'Assigned'), ('PG', 'In progress'), ('SP', 'Stoped'), ('RT', 'Ready to test'), ('TS', 'Testing...'), ('RV', 'To review'), ('RG', 'Revewing...'), ('DN', 'Done'), ('CN', 'Canceled')], default='CR', max_length=2)),
                ('stoped_at', models.DateTimeField(blank=True, null=True)),
                ('marked_ready_to_test_at', models.DateTimeField(blank=True, null=True)),
                ('start_test_at', models.DateTimeField(blank=True, null=True)),
                ('marked_to_reveiw_at', models.DateTimeField(blank=True, null=True)),
                ('start_reveiw_at', models.DateTimeField(blank=True, null=True)),
                ('marked_done_at', models.DateTimeField(blank=True, null=True)),
                ('unused_time', models.DurationField(default=0)),
                ('lost_in_ready_to_test', models.DurationField(default=0)),
                ('lost_in_to_reveiw', models.DurationField(default=0)),
                ('lost_in_stop', models.DurationField(default=0)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
