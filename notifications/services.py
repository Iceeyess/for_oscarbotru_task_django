import re
from smtplib import SMTPServerDisconnected, SMTPResponseException, SMTPRecipientsRefused, SMTPDataError, \
    SMTPNotSupportedError, SMTPHeloError, SMTPConnectError, SMTPSenderRefused, SMTPAuthenticationError

import requests
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.exceptions import ValidationError

from config import settings
from notifications.models import LogInfo


def email_tg_validation(str_obj: str) -> None:
    """Функция валидация данных/шаблонов для сериализатора. Необходимо, чтобы данные были: только цифры или
    формат электронной почты"""
    if not isinstance(str_obj, str) or len(str_obj) > 150:
        raise ValidationError('Получатель должен быть строковым выражением до 150 символов.')
    elif not bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str_obj)) and not str_obj.isdigit():
        raise ValidationError(
            'Получатель должен быть валидным адресом электронной почты или номером Телеграм состоящий только из цифр.')
    elif re.search(r'\s', str_obj):
        raise ValidationError('Получатель не должен содержать пробелы.')


def send_telegram_message(message):
    """Функция отправки сообщений через телеграм, а так же логирования"""

    # Блок проверки статуса
    if not message.log:
        log = LogInfo.objects.create()
        message.log_id = log.id
        message.save()
    elif message.log.code == '200':
        return None
    else:
        log = message.log

    # Блок отправки сообщения
    method = 'sendMessage'
    params = {'chat_id': message.recipient, 'text': message.message}
    url = settings.TG_API_LINK + settings.TG_BOT_TOKEN + '/' + method
    response = requests.get(url, params=params)

    # Проверка статусов отправки и редактирование статусов
    if response.status_code == status.HTTP_200_OK:
        log.status = True
        log.code = status.HTTP_200_OK
        log.save()
    else:
        log.status = False
        log.code = response.status_code
        log.save()


def send_email(message):
    """Функция отправки сообщений через email, а так же логирования"""

    # Блок проверки статуса
    if not message.log:
        log = LogInfo.objects.create()
        message.log_id = log.id
        message.save()
    elif message.log.code == '200':
        return None
    else:
        log = message.log
    # Блок отправки сообщения
    params = {'recipient_list': [message.recipient, ], 'subject': 'Уведомление', 'message': message.message,
              'from_email': settings.EMAIL_HOST_USER, 'fail_silently': False}
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
