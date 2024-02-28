from django.db.models import DecimalField, QuerySet, Sum, functions


class TargetTransactionsQuerySet(QuerySet):
    """Class for custom queryset of `Target` model."""

    def aggregate_targets_sum(self):
        """Method for get amount for targets."""
        return self.aggregate(
            amount_for_targets=functions.Coalesce(
                Sum('amount'),
                0,
                output_field=DecimalField(),
            ),
        )
