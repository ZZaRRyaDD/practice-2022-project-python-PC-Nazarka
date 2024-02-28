from django.urls import path

from . import views


urlpatterns = [
    path('quotes/', views.QuoteAPIView.as_view(), name='quotes'),
]
