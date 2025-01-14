from rest_framework.validators import ValidationError
import re

from notifications.services import email_tg_validation


class IsRecipientStrOrList:

    def __call__(self, values):
        """Валидация данных строки recipients"""
        if not values:
            raise ValidationError('Получатель не должен быть пустым, а содержать строковое выражение или список содержащий строковые выражения до 150 символов.')
        elif isinstance(values, list):
            for val in values:
                email_tg_validation(val)
        elif isinstance(values, str):
            email_tg_validation(values)
        else:
            raise ValidationError('Recipient must be a string or a list of strings.')
