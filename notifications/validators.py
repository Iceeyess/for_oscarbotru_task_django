from rest_framework.validators import ValidationError
from notifications.services import email_tg_validation


class IsRecipientStrOrList:

    def __call__(self, values):
        """Валидация данных строки recipients. Проверяет на """
        if not values:
            raise ValidationError('Получатель не должен быть пустым, а содержать строковое выражение или список '
                                  'содержащий строковые выражения до 150 символов.')
        elif isinstance(values, list):
            for val in values:
                email_tg_validation(val)
        elif isinstance(values, str):
            email_tg_validation(values)
        else:
            raise ValidationError('Recipient поле должно содержать типы строка или список содержащий строки')


class CheckDelay:

    def __call__(self, values):
        """Валидация поля delay на входящие даанные. Только поля с данными (0, 1, 2) могут быть получены."""
        if values not in (0, 1, 2):
            raise ValidationError('В поле delay могут быть только целые числа от 0 до 2.')
