from django.db import models


NULLABLE = dict(null=True, blank=True)


# Create your models here.
class Notification(models.Model):
    """Класс-модель"""
    message = models.CharField(max_length=1024)
    recipient = models.CharField(max_length=150)
    delay = models.IntegerField()
    next_send = models.DateTimeField()
    type = models.CharField(max_length=8)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)