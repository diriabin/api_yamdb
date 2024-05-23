from datetime import datetime

from django.core.exceptions import ValidationError

from reviews.constans import FORBIDDEN_USERNAMES, FORBIDDEN_CHAR


class UsernameRegexValidator():
    def __call__(self, args):
        invalid_chars = []
        for char in args:
            if char in set(FORBIDDEN_CHAR):
                invalid_chars.append(char)
        if invalid_chars:
            msg = f'Имя содержит запрещенные символы {",".join(invalid_chars)}'
            raise ValidationError(msg)


def username_is_not_me(value):
    if value in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Имя пользователя {value} не разрешено.'
        )
    return value


def validate_year(value):
    current_year = datetime.now().year
    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value} больше {current_year}!',
        )
    return value
