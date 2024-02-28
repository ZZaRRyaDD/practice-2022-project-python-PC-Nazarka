from collections import OrderedDict

from rest_framework import serializers

from .target import TargetRetrieveSerializer
from ..constants import errors
from ..models import Target, TargetTransaction
from ...pockets import models


class TargetTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for create TargetTransacton instance."""

    target = serializers.PrimaryKeyRelatedField(
        queryset=Target.objects.all(),
    )

    class Meta:
        model = TargetTransaction
        fields = (
            'target',
            'created_at',
            'amount',
        )

    def validate_amount(self, amount: int) -> int:
        """Validate for `amount` field."""
        user_balance = (
            models.Transaction.objects.get_queryset().get_balance()[
                'balance'
            ]
        )
        if amount > user_balance:
            raise serializers.ValidationError(
                errors.TargetErrors.NOT_CORRECT_INITIAL_DEPOSIT,
            )
        return amount

    def validate_target(
        self,
        target: Target,
    ) -> Target:
        """Method for validate target field."""
        user = self.context['request'].user
        if target not in user.targets.all():
            raise serializers.ValidationError(
                errors.TargetTransactionErrors.NOT_USERS_TARGET,
            )
        return target

    @property
    def data(self) -> OrderedDict:
        return (
            TargetTransactionRetrieveSerializer(instance=self.instance).data
        )


class TargetTransactionRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for TargetTransaction model."""

    target = TargetRetrieveSerializer()

    class Meta:
        model = TargetTransaction
        fields = (
            'id',
            'target',
            'created_at',
            'amount',
        )
