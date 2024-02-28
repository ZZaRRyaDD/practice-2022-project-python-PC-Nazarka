from rest_framework import mixins, viewsets


class ListCreateModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Custom modelviewset with onli `list` and `create` actions."""
    pass
