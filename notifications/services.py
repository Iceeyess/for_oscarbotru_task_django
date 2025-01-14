import re

from rest_framework.exceptions import ValidationError


def email_tg_validation(str_obj: str) -> None:
    if not isinstance(str_obj, str) or len(str_obj) > 150:
        raise ValidationError('Получатель должен быть строковым выражением до 150 символов.')
    elif not bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str_obj)) and not str_obj.isdigit():
        raise ValidationError(
            'Получатель должен быть валидным адресом электронной почты или номером Телеграм состоящий только из цифр.')
    elif re.search(r'\s', str_obj):
        raise ValidationError('Получатель не должен содержать пробелы.')