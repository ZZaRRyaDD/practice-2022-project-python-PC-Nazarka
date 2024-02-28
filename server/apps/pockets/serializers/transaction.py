from collections import OrderedDict

from rest_framework import serializers

from .transaction_category import (
    TransactionCategoryRetrieveSerializer,
    TransactionCategorySerializer,
)
from ..constants import TransactionErrors, TransactionTypes
from ..models import Transaction, TransactionCategory


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'category',
            'transaction_date',
            'amount',
            'transaction_type',
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Transaction
        fields = (
            'id',
            'category',
            'transaction_date',
            'amount',
            'transaction_type',
        )

    def validate_category(
        self,
        category: TransactionCategory,
    ) -> TransactionCategory:
        data = self.get_initial()
        if data['transaction_type'] == TransactionTypes.INCOME:
            if category is not None:
                raise serializers.ValidationError(
                    TransactionErrors.INCOME_CANT_HAVE_CATEGORY,
                )

        if data['transaction_type'] == TransactionTypes.EXPENSE:
            user = self.context['request'].user
            if category not in user.categories.all():
                raise serializers.ValidationError(
                    TransactionErrors.NOT_USERS_CATEGORY,
                )
        return category

    def create(self, validated_data: dict) -> Transaction:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        Сделано для того, чтобы при создании объекта можно было передвавть id категории, а после
        создания поле категории возвращалось как объект
        """
        return TransactionRetrieveSerializer(instance=self.instance).data


class TransactionGlobalSerializer(serializers.Serializer):
    """Serializer for total info and user transactions."""

    total_income = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    total_expenses = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    amount_for_targets = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    expense_category = TransactionCategoryRetrieveSerializer(
        allow_null=True,
    )


class TransactionBalanceSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
