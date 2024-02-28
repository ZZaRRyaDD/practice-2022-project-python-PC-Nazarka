from django.urls import path

from . import views


urlpatterns = [
    path(
        'pockets/global/',
        views.TotalInfoTransactionsAPIView.as_view(),
        name='global',
    ),
]
