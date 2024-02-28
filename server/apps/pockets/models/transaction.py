from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .managers import TransactionManager
from .transaction_category import TransactionCategory
from ..constants import TransactionTypes


class Transaction(models.Model):
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Пользователь',
    )
    category = models.ForeignKey(
        to='pockets.TransactionCategory',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    transaction_date = models.DateField(
        verbose_name='Дата операции',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма операции',
        validators=(MinValueValidator(Decimal('0.01')),),
    )
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionTypes.CHOICES,
        verbose_name='Тип операции',
    )

    objects = TransactionManager()

    def __str__(self) -> str:
        return (
            f'{self.category} '
            f'{self.amount} '
            f'({TransactionTypes.CHOICES_DICT[self.transaction_type]})'
        )

    @staticmethod
    def create_transactions(append_transactions: list, user) -> None:
        """Create more one transactions."""
        Transaction.objects.bulk_create(
            [
                Transaction(
                    transaction_date=data['transaction_date'],
                    amount=data['amount'],
                    transaction_type=data['transaction_type'],
                    category=(
                        None
                        if data['category'] is None
                        else TransactionCategory.objects.filter(
                            name=data['category'],
                        ).first()
                    ),
                    user=user,
                )
                for data in append_transactions
            ],
        )

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
