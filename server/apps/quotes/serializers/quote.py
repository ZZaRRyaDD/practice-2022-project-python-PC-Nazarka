from rest_framework import serializers

from ..models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for Quote model."""

    class Meta:
        model = Quote
        fields = (
            'id',
            'text',
            'author',
        )
