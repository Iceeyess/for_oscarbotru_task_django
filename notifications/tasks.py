from config.settings import TIME_ZONE
from notifications.models import Notification
from datetime import datetime
from celery import shared_task
from pytz import timezone
from notifications.services import send_telegram_message, send_email


@shared_task
def send_messages() -> None:
    """Функция-задача
    """
    messages = Notification.objects.filter(next_send__lte=datetime.now(timezone(TIME_ZONE)))
    #  Отправляет сообщение пользователю в телеграм
    for message in messages:
        if message.type == 'telegram':
            send_telegram_message(message)
        elif message.type == 'email':
            send_email(message)


