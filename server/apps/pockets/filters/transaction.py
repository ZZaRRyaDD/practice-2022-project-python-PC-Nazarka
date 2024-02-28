from django_filters import rest_framework as filters

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    """Filter for transaction by category name, year, month."""

    category__name = filters.CharFilter(
        lookup_expr='icontains',
    )
    transaction_date_year = filters.NumberFilter(
        field_name='transaction_date',
        lookup_expr='year__exact',
    )
    transaction_date_month = filters.NumberFilter(
        field_name='transaction_date',
        lookup_expr='month__exact',
    )
    ordering = filters.OrderingFilter(
        fields=(
            ('transaction_date', 'date'),
            ('category__name', 'category'),
            ('amount', 'amount'),
            ('transaction_type', 'transaction_type'),
        ),
    )

    class Meta:
        model = Transaction
        fields = ('category', 'transaction_date')
