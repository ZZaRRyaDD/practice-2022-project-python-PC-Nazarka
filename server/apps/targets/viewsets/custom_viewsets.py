from rest_framework import mixins, viewsets


class CreateListUpdateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Custom viewset for `create`, `list`, `update`, `delete` actions."""
    pass


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Custom viewset for `create` action."""
    pass
