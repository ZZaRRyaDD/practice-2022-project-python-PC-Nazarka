from rest_framework import response, status, views

from .. import models, serializers


class QuoteAPIView(views.APIView):
    """View-controller for return random quote."""

    def get(self, request, *args, **kwargs) -> response.Response:
        """Handler for get request."""
        return response.Response(
            data=serializers.QuoteSerializer(
                models.Quote.objects.order_by('?').first(),
            ).data,
            status=status.HTTP_200_OK,
        )
