from django.core.exceptions import ValidationError


def name_is_not_me(name):
    if name.lower() == 'me':
        raise ValidationError(
            (f'{name} использовать запрещено'), params={"name": name}
        )
