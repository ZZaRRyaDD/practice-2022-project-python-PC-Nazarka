from django.db import models


class Quote(models.Model):
    """Model for Quote."""

    text = models.TextField(
        verbose_name='Текст цитаты',
    )
    author = models.CharField(
        max_length=128,
        verbose_name='Автор цитаты',
    )

    def __str__(self) -> str:
        return f'"{self.text}" {self.author}'

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        unique_together = ('text', 'author')
