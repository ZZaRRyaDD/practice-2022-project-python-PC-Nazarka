from rest_framework import response, status, views

from ..models import Transaction, TransactionCategory
from ..serializers import (
    TransactionGlobalSerializer,
)
from ...targets import models


class TotalInfoTransactionsAPIView(views.APIView):
    """View-controller for return global info about pocket."""

    def get(self, request, *args, **kwargs):
        """Handler for get request."""
        data = {
            'expense_category': (
                TransactionCategory.objects.get_expenses_category(
                    request.user,
                )
            ),
        }
        data.update(
            Transaction.objects.transaction_sums_by_last_month(
                request.user,
            ),
        )
        data.update(
            models.TargetTransaction.objects.get_amount_for_targets(
                request.user,
            ),
        )
        serializer = TransactionGlobalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
