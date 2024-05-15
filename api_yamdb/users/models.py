from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(verbose_name='биография', null=True, blank=True)
    role = models.CharField(
        default='user', choices=(
            ('user', 'user'),
            ('moderator', 'moderator'),
            ('admin', 'admin'),
        ), verbose_name='роль', max_length=10
    )

    def __str__(self):
        return self.username
