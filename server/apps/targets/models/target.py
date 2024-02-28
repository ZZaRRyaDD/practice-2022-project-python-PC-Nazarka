import datetime
from decimal import Decimal
from typing import Union

from django.core.validators import MinValueValidator
from django.db import models

from .managers import TargetManager
from ..constants import MIN_COUNT_MONTHS


class Target(models.Model):
    """Model for Target."""

    name = models.CharField(
        max_length=128,
        verbose_name='Имя цели',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма цели',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='targets',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    initial_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Начальный вклад',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    deposit_term = models.PositiveIntegerField(
        validators=(MinValueValidator(MIN_COUNT_MONTHS),),
        verbose_name='Срок(месяцы)',
    )
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=(
            MinValueValidator(Decimal('0.01')),
        ),
        verbose_name='Процент',
    )
    created_at = models.DateField(
        verbose_name='Дата создания цели',
        default=datetime.date.today,
    )
    is_finished = models.BooleanField(
        verbose_name='Завершена ли цель',
        default=False,
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='targets',
        verbose_name='Пользователь',
    )

    objects = TargetManager()

    @property
    def current_amount(self):
        """Return balance of target."""
        return self.transactions.all().aggregate(models.Sum('amount'))[
            'amount__sum'
        ]

    @property
    def percentage_completion(self) -> Union[float, int]:
        """Returns the percentage remaining until completion."""
        return 100 - (self.current_amount/self.amount) * 100

    @property
    def count_days_to_end(self):
        """Return count days to end of target."""
        return (self.created_at - datetime.date.today()).days

    def __str__(self) -> str:
        return f'{self.name} {self.amount}'

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ('created_at', )
