from datetime import datetime

from django.core.exceptions import ValidationError

from reviews.constans import FORBIDDEN_USERNAMES

import re


def validate_username(username):
    forbidden_chars = re.findall(r'[^\w.@+-]', username)
    if forbidden_chars:
        raise ValidationError(
            f'Недопустимые символы в имени: {forbidden_chars}'
        )
    return username


def username_is_not_forbidden(username):
    if username in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {username} не разрешено.'
        )
    return username


def validate_year(year):
    current_year = datetime.now().year
    if year >= datetime.now().year:
        raise ValidationError(
            message=f'Год {year} больше {current_year}!',
        )
    return year
