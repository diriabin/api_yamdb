from django.core.exceptions import ValidationError


def name_is_not_me(name):
    if name.title() == 'Me':
        raise ValidationError(
            (f'{name} использовать запрещено'), params={"name": name}
        )
