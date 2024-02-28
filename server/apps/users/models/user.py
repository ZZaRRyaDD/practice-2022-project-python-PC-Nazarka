from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username} ({self.email})'

    def save(self, *args, **kwargs):
        is_created = self.id is None
        super().save(*args, **kwargs)

        if is_created:
            Token.objects.create(user=self)
