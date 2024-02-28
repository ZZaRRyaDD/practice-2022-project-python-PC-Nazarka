import datetime

from rest_framework import pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .custom_viewsets import CreateViewSet
from ..models import Target, TargetTransaction
from ..serializers import TargetTransactionCreateSerializer
from ...pockets import constants, models


class TargetTransactionViewSet(CreateViewSet):
    """ViewSet for TargetTransaction model."""

    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (permissions.IsAuthenticated,)
    queryset = TargetTransaction.objects.all()

    @action(methods=('POST',), detail=False)
    def replenishment(self, request) -> Response:
        """Action for replenishment balance of target."""
        serializer = TargetTransactionCreateSerializer(
            data=request.data,
            context={
                'request': request,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        target = Target.objects.get(id=request.data['target'])
        models.Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=request.data['amount'],
            transaction_type=(
                constants.transaction.TransactionTypes.EXPENSE
            ),
            category=target.category,
            user=target.user,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
