from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0
    message = ('Введите правильное имя пользователя. Оно может содержать'
               ' только буквы, цифры и знаки @/./+/-/_.')
    error_messages = {
        'invalid': 'Только буквы, цифры и @/./+/-/_',
        'required': 'Поле не может быть пустым',
    }


def username_is_not_me(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value


def validate_year(value):
    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value} больше текущего!',
            params={'value': value},
        )
