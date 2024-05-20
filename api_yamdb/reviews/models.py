from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .constans import SLICE_STR, MAX_LENGTH_SLUG, MAX_LENGTH_CHAR

User = get_user_model()


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
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название'
                            )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.CharField(
        max_length=MAX_LENGTH_CHAR, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        # on_delete=models.SET_NULL,
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
        unique_together = ['name', 'year']

    def __str__(self):
        return self.name[:SLICE_STR]


class Review(models.Model):
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

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
