from datetime import datetime
import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(username):
    forbidden_chars = re.findall(r'[^\w.@+-]', username)
    if forbidden_chars:
        raise ValidationError(
            f'Недопустимые символы в имени: {forbidden_chars}'
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
    if year >= datetime.now().year:
        raise ValidationError(
            message=f'Год {year} больше {current_year}!',
        )
    return year
