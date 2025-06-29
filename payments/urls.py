from django.urls import path
from .views import (
    PaymentListView,
    PaymentCreateView,
    PaymentDetailView,
    PaymentDeleteView
)

app_name = 'payments'

urlpatterns = [
    path(
        '',
        PaymentListView.as_view(),
        name='payment-list'
    ),
    path(
        'create/',
        PaymentCreateView.as_view(),
        name='payment-create'
    ),
    path(
        '<int:pk>/',
        PaymentDetailView.as_view(),
        name='payment-detail'
    ),
    path(
        '<int:pk>/delete/',
        PaymentDeleteView.as_view(),
        name='payment-delete'
    ),
]
