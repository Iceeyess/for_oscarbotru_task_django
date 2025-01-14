from smtplib import SMTPServerDisconnected, SMTPResponseException, SMTPRecipientsRefused, SMTPDataError, \
    SMTPNotSupportedError, SMTPHeloError, SMTPConnectError, SMTPSenderRefused, SMTPAuthenticationError

from rest_framework import status
from config import settings
from config.settings import TIME_ZONE
from notifications.models import Notification, LogInfo
from datetime import datetime
import requests
from celery import shared_task
from django.core.mail import send_mail
from pytz import timezone

@shared_task
def send_messages() -> None:
    """Функция отправки сообщений.
    В зависимости от того, какой тип мессаджера был сохранен в БД, используется та система отправки по API"""
    messages = Notification.objects.filter(next_send__lte=datetime.datetime.now(timezone(TIME_ZONE)))
    #  Отправляет сообщение пользователю в телеграм
    for message in messages:
        if message.type == 'telegram':
            method = 'sendMessage'
            params = {'chat_id': message.recipient, 'text': message}
            url = settings.TG_API_LINK + settings.TG_BOT_TOKEN + '/' + method
            response = requests.get(url, params=params)
            log = LogInfo.objects.create()
            message.log_id = log.id
            message.save()
            if response.status_code == status.HTTP_200_OK:
                log.status = status.HTTP_200_OK
                log.save()
            else:
                log.status = response.status_code
                log.save()
        elif message.type == 'email':
            params = {'recipient_list': [message.recipient, ],'subject': 'Уведомление', 'message': message.message,
                      'from_email': settings.EMAIL_HOST_USER, 'fail_silently': False}
            log = LogInfo.objects.create()
            message.log_id = log.id
            message.save()
            # Блок отправки сообщения
            try:
                send_mail(**params)
                log.status = True
                log.code = status.HTTP_200_OK
                log.save()
            except (SMTPServerDisconnected, SMTPResponseException, SMTPRecipientsRefused, SMTPDataError,
                        SMTPConnectError, SMTPHeloError, SMTPNotSupportedError):
                log.status = False
                log.code = status.HTTP_500_INTERNAL_SERVER_ERROR
                log.save()
            except (SMTPSenderRefused, SMTPAuthenticationError):
                log.status = False
                log.code = status.HTTP_403_FORBIDDEN
                log.save()


