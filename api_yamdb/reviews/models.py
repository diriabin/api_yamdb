from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from .constans import (SLICE_STR, MAX_LENGTH_SLUG, MAX_LENGTH_CHAR,
                       MAX_LENGTH_USERNAME, MAX_LENGTH_NAMES,
                       MIN_REVIEW_SCORE, MAX_REVIEW_SCORE, CONF_CODE_MAX_LEN)
from .validators import (validate_username, username_is_not_me,
                         validate_year)


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
        validators=(validate_username, username_is_not_me,),
        verbose_name='имя пользователя',
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email адрес'
    )
    role = models.CharField(
        default=USER,
        choices=ROLES,
        max_length=max(len(role) for role, _ in ROLES),
        verbose_name='роль'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAMES,
        blank=True,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAMES,
        blank=True,
        verbose_name='фамилия'
    )
    confirmation_code = models.CharField(
        max_length=CONF_CODE_MAX_LEN,
        null=True,
        blank=False,
        default='XXXX',
        verbose_name='код подтверждения'
    )

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        unique_together = ('email', 'username',)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username[:SLICE_STR]


class CategoryGenreBased(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:SLICE_STR]


class Category(CategoryGenreBased):

    class Meta(CategoryGenreBased.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBased):

    class Meta(CategoryGenreBased.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска'
    )
    description = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)
        unique_together = ('name', 'year',)

    def __str__(self):
        return self.name[:SLICE_STR]


class ReviewCommentBased(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:SLICE_STR]


class Review(ReviewCommentBased):
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_REVIEW_SCORE),
                    MaxValueValidator(MAX_REVIEW_SCORE)],
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta(ReviewCommentBased.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        unique_together = ('title', 'author',)


class Comment(ReviewCommentBased):
    text = models.TextField(
        verbose_name='Текст'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBased.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
