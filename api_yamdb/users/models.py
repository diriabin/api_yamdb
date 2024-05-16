from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(verbose_name='биография', null=True, blank=True)
    email = models.EmailField('email адрес')
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
