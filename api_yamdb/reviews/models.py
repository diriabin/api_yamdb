from django.db import models


class Title(models.Model):
    name = models.CharField(unique=True, max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.CharField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанры',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:20]
