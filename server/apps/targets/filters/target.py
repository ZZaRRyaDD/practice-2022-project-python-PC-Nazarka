from django_filters import rest_framework as filters

from ..models import Target


class TargetFilter(filters.FilterSet):
    """Filter for target."""

    ordering = filters.OrderingFilter(
        fields=(
            ('percent', 'percent'),
            ('created_at', 'date'),
            ('amount', 'amount'),
            ('count_days_to_end', 'days_to_end'),
        ),
    )

    class Meta:
        model = Target
        fields = ('percent', 'created_at', 'amount')
