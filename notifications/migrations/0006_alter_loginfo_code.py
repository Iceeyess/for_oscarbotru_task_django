# Generated by Django 5.1.4 on 2025-01-14 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_loginfo_remove_notification_status_notification_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginfo',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]