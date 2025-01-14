import re

from django.db.transaction import commit
from rest_framework import serializers

from notifications.models import Notification
from notifications.validators import IsRecipientStrOrList


class NotificationSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    message = serializers.CharField(max_length=1024)
    recipient = serializers.CharField(max_length=150, validators=[IsRecipientStrOrList(), ])
    delay = serializers.IntegerField()

    def create(self, validated_data):
        if validated_data.get('recipient').isdigit():
            validated_data['type'] = 'telegram'
        elif bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', validated_data.get('recipient'))):
            validated_data['type'] = 'email'
        return Notification.objects.create(**validated_data)





