from rest_framework.routers import DefaultRouter

from .viewsets import TargetTransactionViewSet, TargetViewSet

targets_router = DefaultRouter()

targets_router.register(
    prefix='targets',
    viewset=TargetViewSet,
    basename='targets',
)

targets_router.register(
    prefix='target_transactions',
    viewset=TargetTransactionViewSet,
    basename='target_transactions',
)
