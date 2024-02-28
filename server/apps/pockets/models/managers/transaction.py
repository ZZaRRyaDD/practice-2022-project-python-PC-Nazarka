from decimal import Decimal

from django.db.models import Manager
from django.utils import timezone

from ..querysets import TransactionQuerySet


class TransactionManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionQuerySet:
        return TransactionQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_transaction_sums(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()

    def transaction_sums_by_last_month(
        self,
        user,
    ) -> dict[str, Decimal]:
        return self.filter(
            user=user,
            transaction_date__month=timezone.now().month,
            transaction_date__year=timezone.now().year,
        ).aggregate_totals()
