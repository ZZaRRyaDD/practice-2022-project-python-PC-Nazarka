from typing import Type

from django.db.models import QuerySet

from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


from .custom_viewsets import ListCreateModelViewSet
from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategoryTransactionSumSerializer,
)


class TransactionCategoryViewSet(ListCreateModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter, )
    ordering_fields = ('transactions_sum', )

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action in ('transactions_by_categories', 'top_categories'):
            serializer_class = TransactionCategoryTransactionSumSerializer
        else:
            serializer_class = TransactionCategorySerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).order_by(
            '-id',
        )
        if self.action in ('transactions_by_categories', 'top_categories'):
            queryset = queryset.annotate_with_transaction_sums().order_by(
                '-transactions_sum',
            )

        return queryset

    @action(
        methods=('GET',),
        detail=False,
        url_path='transactions-by-categories',
    )
    def transactions_by_categories(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        return super().list(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='top-categories')
    def top_categories(self, request: Request, *args, **kwargs) -> Response:
        return Response(
            data=self.get_queryset().get_top_categories(),
            status=status.HTTP_200_OK,
        )
