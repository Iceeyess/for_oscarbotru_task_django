# Generated by Django 5.1.4 on 2025-01-14 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notification_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('code', models.IntegerField()),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='status',
        ),
        migrations.AddField(
            model_name='notification',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notifications.loginfo'),
        ),
    ]