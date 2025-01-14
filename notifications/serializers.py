import re
import datetime
from pytz import timezone
from config.settings import TIME_ZONE
from django.db.transaction import commit
from rest_framework import serializers
from notifications.models import Notification
from notifications.validators import IsRecipientStrOrList, CheckDelay


class NotificationSerializer(serializers.Serializer):
    """Класс сериализатора"""
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    message = serializers.CharField(max_length=1024)
    recipient = serializers.CharField(max_length=150, validators=[IsRecipientStrOrList(), ])
    delay = serializers.IntegerField(validators=[CheckDelay(), ])

    def create(self, validated_data):
        """Создание в БД объектов, а так же заполнение в БД поля типа recipient(email, telegram).
        Кроме того сохраняется параметр next_send на основании условий из задания, где:
        0 - текущий момент, 1 - задержка на час, 2 - задержка на день."""
        delay = {0: datetime.datetime.now(timezone(TIME_ZONE)), 1:datetime.datetime.now(timezone(TIME_ZONE)) + datetime.timedelta(hours=1),
                 2:datetime.datetime.now(timezone(TIME_ZONE)) + datetime.timedelta(days=1)}
        if validated_data.get('recipient').isdigit():
            validated_data['type'] = 'telegram'
        elif bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', validated_data.get('recipient'))):
            validated_data['type'] = 'email'
        validated_data['next_send'] = delay.get(validated_data['delay'])
        return Notification.objects.create(**validated_data)





