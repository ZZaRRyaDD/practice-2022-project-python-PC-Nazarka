from django.urls import path

from apps.users.views import UserCreateAPIView

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


urlpatterns = [
    path(
        'register/',
        UserCreateAPIView.as_view(),
    ),
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]
