import datetime
from typing import Type

from rest_framework import pagination, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .custom_viewsets import CreateListUpdateDeleteViewSet
from ..filters import TargetFilter, filters
from ..functions import get_user_analytics
from ..models import Target, TargetTransaction
from ..permissions import TargetPermissions
from ..serializers import (
    TargetCreateSerializer,
    TargetFinishSerializer,
    TargetRetrieveSerializer,
)
from ...pockets import constants, models


class TargetViewSet(CreateListUpdateDeleteViewSet):
    """ViewSet for Target model."""

    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (permissions.IsAuthenticated, TargetPermissions)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TargetFilter
    queryset = Target.objects.all()

    def perform_create(self, serializer):
        """
        Method for create target and create transaction and target-transaction.
        """
        serializer.save()
        if serializer.data['initial_deposit']:
            models.Transaction.objects.create(
                transaction_date=datetime.date.today(),
                amount=serializer.data['initial_deposit'],
                transaction_type=(
                    constants.transaction.TransactionTypes.EXPENSE
                ),
                category=models.TransactionCategory.objects.get(
                    id=serializer.data['category']['id'],
                ),
                user=Target.objects.get(id=serializer.data['id']).user,
            )
            TargetTransaction.objects.create(
                target=Target.objects.get(id=serializer.data['id']),
                amount=serializer.data['initial_deposit'],
            )

    def perform_destroy(self, instance):
        """Method for delete target and create transaction."""
        if instance.current_amount < instance.amount:
            models.Transaction.objects.create(
                transaction_date=datetime.date.today(),
                amount=instance.current_amount,
                transaction_type=(
                    constants.transaction.TransactionTypes.INCOME
                ),
                category=instance.category,
                user=instance.user,
            )
        instance.delete()

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        """Method for get serializer class."""
        if self.action in ('create', 'update'):
            return TargetCreateSerializer
        elif self.action == 'finish':
            return TargetFinishSerializer
        return TargetRetrieveSerializer

    @action(methods=('POST',), detail=True)
    def finish(self, request, pk: int = None) -> Response:
        """Action for finish target."""
        target = self.get_object()
        serializer = TargetFinishSerializer(data={
            'target': target.id,
        })
        serializer.is_valid(raise_exception=True)
        models.Transaction.objects.create(
            transaction_date=datetime.date.today(),
            amount=target.current_amount,
            transaction_type=(
                constants.transaction.TransactionTypes.INCOME
            ),
            category=target.category,
            user=target.user,
        )
        return Response(
            data={
                'message': 'Цель завершена',
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=('GET',), detail=False, url_path='analytics')
    def analytics(self, request: Request, *args, **kwargs) -> Response:
        """Action for return analytics of user's targets."""
        return Response(
            data=get_user_analytics(request.user),
            status=status.HTTP_200_OK,
        )

    @action(methods=('GET',), detail=False, url_path='top-targets')
    def top_targets(self, request: Request, *args, **kwargs) -> Response:
        """Action for return top targets close to completion."""
        return Response(
            self.get_queryset().get_top_targets(),
            status=status.HTTP_200_OK,
        )
