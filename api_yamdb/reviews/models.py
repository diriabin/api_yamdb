from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from .constans import (SLICE_STR, MAX_LENGTH_SLUG, MAX_LENGTH_CHAR,
                      MAX_LENGTH_USERNAME)
from .validators import UsernameRegexValidator, username_is_not_me


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=(UsernameRegexValidator(), username_is_not_me),
        verbose_name='имя пользователя',
    )
    bio = models.TextField(
        verbose_name='биография', null=True, blank=True
    )
    email = models.EmailField(
        verbose_name='email адрес', unique=True
    )
    role = models.CharField(
        default=USER,
        choices=ROLES,
        verbose_name='роль',
        max_length=max(len(role) for role, _ in ROLES),

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

    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('email', 'username',)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username[:20]


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG, unique=True, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name[:SLICE_STR]


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_CHAR, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG, unique=True, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name[:SLICE_STR]


class Title(models.Model):
    name = models.CharField(
        unique=True, max_length=MAX_LENGTH_CHAR, verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:SLICE_STR]


class Review(models.Model):
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author',)

    def __str__(self):
        return self.text[:SLICE_STR]


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id']

    def __str__(self):
        return self.text[:SLICE_STR]
