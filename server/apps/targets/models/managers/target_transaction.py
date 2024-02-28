from django.db.models import Manager
from django.utils import timezone

from ..querysets import TargetTransactionsQuerySet


class TargetTransactionsManager(Manager):
    """Class for custom manager of `TargetTransactions` model."""

    def get_queryset(self, **kwargs):
        return TargetTransactionsQuerySet(
            self.model,
            using=self._db,
        )

    def get_amount_for_targets(self, user):
        return self.filter(
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
            target__user=user,
        ).aggregate_targets_sum()
