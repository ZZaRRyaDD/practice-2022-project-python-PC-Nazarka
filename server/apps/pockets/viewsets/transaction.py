from datetime import date
from decimal import Decimal
from tempfile import NamedTemporaryFile
from typing import Type, Union

from django.core.files.base import ContentFile
from django.http import HttpResponse

from rest_framework import pagination, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


from ..filters import TransactionFilter, filters
from ..functions import export_operation, import_operation
from ..models import Transaction
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    TransactionBalanceSerializer,
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TransactionFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == 'balance':
            serializer_class = TransactionBalanceSerializer
        elif self.action in {'create', 'update', 'partial_update'}:
            serializer_class = TransactionCreateSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:
        return Transaction.objects.filter(
            user=self.request.user,
        ).select_related(
            'category',
        ).order_by(
            '-transaction_date', '-id',
        )

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        if self.action == 'balance':
            obj = self.get_queryset().get_balance()
        else:
            obj = super().get_object()
        return obj

    @action(methods=('GET',), detail=False, url_path='balance')
    def balance(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='export')
    def export_transactions(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """Action for export transactions and categories."""
        with NamedTemporaryFile() as file_obj:
            export_operation(
                self.get_queryset(),
                file_obj.name,
            )
            file_to_send = ContentFile(file_obj.read())
            filename = f'Transactions-{request.user.username}-{date.today()}'
            response = HttpResponse(file_to_send, 'application/x-gzip')
            response['Content-Length'] = file_to_send.size
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}.xlsx"'
            )
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response

    @action(methods=('POST',), detail=False, url_path='import')
    def import_transactions(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """Action for import transactions and categories."""
        data = import_operation(request)
        if 'message' not in data:
            return Response(
                data=data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
