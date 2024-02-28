import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .managers import TargetTransactionsManager
from .target import Target


class TargetTransaction(models.Model):
    """Model for TargetTransaction."""

    target = models.ForeignKey(
        to='targets.Target',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Цель',
    )
    created_at = models.DateField(
        verbose_name='Дата операции',
        default=datetime.date.today,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Изменение баланса',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    from_percent = models.BooleanField(
        verbose_name='Пришли ли деньги с процентов',
        default=False,
    )

    objects = TargetTransactionsManager()

    def __str__(self) -> str:
        return f'{self.target.name} {self.created_at} {self.amount}'

    @staticmethod
    def interest_append() -> None:
        """Staticmethod for interest append."""
        TargetTransaction.objects.bulk_create(
            [
                TargetTransaction(
                    target=target,
                    amount=(target.current_amount * target.percent / 36500),
                    from_percent=True,
                )
                for target in Target.objects.filter(is_finished=False)
            ],
        )

    class Meta:
        verbose_name = 'Операция цели'
        verbose_name_plural = 'Операции целей'
