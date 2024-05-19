from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import name_is_not_me


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(), name_is_not_me),
        verbose_name='имя пользователя',
    )
    bio = models.TextField(verbose_name='биография', null=True, blank=True)
    email = models.EmailField(verbose_name='email адрес',
                              unique=True)
    password = None
    role = models.CharField(
        default='user',
        choices=(
            ('user', 'Пользователь'),
            ('moderator', 'Модератор'),
            ('admin', 'Админ'),

        ),
        verbose_name='роль',
        max_length=10,

    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        if not self.role == "user":
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username[:20]


class СonfirmationСode(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)
    code = models.IntegerField(default=None, null=True)
