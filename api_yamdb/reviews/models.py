from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        max_length=256, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Comments(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    title_id = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='comments'
    )
    review_id = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id']

    def __str__(self):
        return self.text
