from collections import OrderedDict
from datetime import date

from rest_framework import serializers

from ..constants import errors
from ..functions import add_months, calculate_count_month
from ..models import Target
from ...pockets import constants, models, serializers as pocket_serializers


class TargetCreateSerializer(serializers.ModelSerializer):
    """Serializer for create Target instance."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.TransactionCategory.objects.all(),
    )

    class Meta:
        model = Target
        fields = (
            'name',
            'amount',
            'category',
            'initial_deposit',
            'deposit_term',
            'percent',
            'created_at',
            'is_finished',
        )

    def validate_deposit_term(
        self,
        deposit_term: int,
    ) -> int:
        """Method for validate deposit term field."""
        instance = getattr(self, 'instance', None)
        if instance is not None:
            old_date = add_months(instance.created_at, instance.deposit_term)
            new_date = add_months(date.today(), deposit_term)
            if old_date > new_date:
                raise serializers.ValidationError(
                    errors.TargetErrors.CHANGE_DEPOSIT_TERM,
                )
            deposit_term += calculate_count_month(instance.created_at)
        return deposit_term

    def validate_initial_deposit(
        self,
        initial_deposit: int,
    ) -> int:
        """Method for validate initial_deposit field."""
        instance = getattr(self, 'instance', None)
        if instance is None:
            user_balance = (
                models.Transaction.objects.get_queryset().get_balance()[
                    'balance'
                ]
            )
            if initial_deposit > user_balance:
                raise serializers.ValidationError(
                    errors.TargetErrors.NOT_CORRECT_INITIAL_DEPOSIT,
                )
        return initial_deposit

    def validate_amount(
        self,
        amount: int,
    ) -> int:
        """Method for validate amount field."""
        instance = getattr(self, 'instance', None)
        if instance is not None and instance.amount > amount:
            raise serializers.ValidationError(
                errors.TargetErrors.CHANGE_TARGET_AMOUNT,
            )
        return amount

    def validate_category(
        self,
        category: models.TransactionCategory,
    ) -> models.TransactionCategory:
        """Method for validate category field."""
        user = self.context['request'].user
        if category not in user.categories.all():
            raise serializers.ValidationError(
                constants.errors.TransactionErrors.NOT_USERS_CATEGORY,
            )
        return category

    def create(self, validated_data: dict) -> Target:
        """Method for create instance with get user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        return TargetRetrieveSerializer(instance=self.instance).data


class TargetRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for Target model."""

    category = pocket_serializers.TransactionCategorySerializer()
    amount_for_last_month = serializers.SerializerMethodField(
        'get_amount_for_last_month',
    )

    def get_amount_for_last_month(self, obj):
        """Get amount for last month."""
        return Target.objects.filter(
            id=obj.id,
        ).get_income_percent_month()[
            'income_percent_month'
        ]

    class Meta:
        model = Target
        fields = (
            'id',
            'name',
            'amount',
            'category',
            'initial_deposit',
            'deposit_term',
            'percent',
            'created_at',
            'current_amount',
            'amount_for_last_month',
            'count_days_to_end',
            'is_finished',
        )


class TargetFinishSerializer(serializers.Serializer):
    """Serializer for check finishing of target."""

    target = serializers.PrimaryKeyRelatedField(
        queryset=Target.objects.all(),
    )

    def validate_target(self, target: Target) -> Target:
        """Method for validate `target` field."""
        if target.current_amount < target.amount:
            raise serializers.ValidationError(
                errors.TargetErrors.REQUIRED_AMOUNT,
            )
        return target
