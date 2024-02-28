from decimal import Decimal

from django.db.models import DecimalField, QuerySet, Sum, functions
from django.utils import timezone

from .. import target_transaction


class TargetQuerySet(QuerySet):
    """Class for custom queryset of `Target` model."""

    def get_immediate_target(self):
        """Method for get immediate target of queryset."""
        immediate_target = sorted(
            self,
            key=lambda t: t.count_days_to_end,
        )
        return (
            immediate_target[0].count_days_to_end
            if immediate_target else None
        )

    def get_all_income_percent(self) -> dict[str, Decimal]:
        """Method for get all income percent of targets."""
        return target_transaction.TargetTransaction.objects.filter(
            target__in=self,
            from_percent=True,
        ).aggregate(
            all_income_percent=functions.Coalesce(
                Sum('amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_amount_not_finished_targets(self) -> dict[str, Decimal]:
        """Method for get amount not finished targets."""
        return target_transaction.TargetTransaction.objects.filter(
            target__in=self,
            from_percent=True,
        ).aggregate(
            amount_not_finished_targets=functions.Coalesce(
                Sum('amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_income_percent_month(self) -> dict[str, Decimal]:
        """Method for get income percent month of targets."""
        return target_transaction.TargetTransaction.objects.filter(
            target__in=self,
            from_percent=True,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        ).aggregate(
            income_percent_month=functions.Coalesce(
                Sum('amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_top_targets(self) -> 'TargetQuerySet':
        """Method for return top targets close to completion."""
        targets = sorted(
            self,
            key=lambda x: x.percentage_completion,
        )[:3]
        return target_transaction.Target.objects.filter(
            id__in=map(lambda x: x.id, targets),
        ).values()
