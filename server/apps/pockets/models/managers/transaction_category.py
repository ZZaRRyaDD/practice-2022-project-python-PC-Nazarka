from django.db.models import Manager
from django.utils import timezone

from ..querysets import TransactionCategoryQuerySet


class TransactionCategoryManager(Manager):
    """Custom manager for `TransactionCategory`."""

    def get_queryset(self, **kwargs) -> TransactionCategoryQuerySet:
        return TransactionCategoryQuerySet(self.model, using=self._db)

    def annotate_with_transaction_sums(self) -> 'TransactionCategoryQuerySet':
        return self.get_queryset().annotate_with_transaction_sums()

    def get_expenses_category(self, user):
        """Method for get three expenses categories."""
        expense_category = self.filter(
            user=user,
            transactions__transaction_date__month=timezone.now().month,
            transactions__transaction_date__year=timezone.now().year,
        ).order_by('-transactions__amount')
        return expense_category.values()[0] if expense_category else None
