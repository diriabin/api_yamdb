from datetime import datetime
import re

from django.conf import settings
from django.core.exceptions import ValidationError

from api_yamdb.settings import REGULAR_WITH_INVALID_CHARS


def validate_username(username):
    forbidden_chars = re.findall(r'[^\w.@+-]', username)
    if forbidden_chars:
        raise ValidationError(
            f'Недопустимые символы в имени: {set(forbidden_chars)}'
        )
    return username


def username_is_not_forbidden(value):
    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {value} не разрешено.'
        )
    return value


def validate_year(year):
    current_year = datetime.now().year
    if year >= current_year:
        raise ValidationError(
            message=f'Год {year} больше {current_year}!',
        )
    return year


def validate_confirmation_code(pin_code):
    invalid_chars = re.findall(
        REGULAR_WITH_INVALID_CHARS, pin_code
    )
    if invalid_chars:
        raise ValidationError(
            f'Код не должен содержать символы {invalid_chars}'
        )
    return pin_code
