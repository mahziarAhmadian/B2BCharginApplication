from django.urls import path
from ..views import transaction_views

app_name = "api-v1-transaction"

urlpatterns = [
    path(
        "seller/sell",
        transaction_views.TransferAPIView.as_view(),
        name="sell",
    ),
    path(
        "admin/",
        transaction_views.TransactionViewSet.as_view({
            'get': 'list',
        }),
        name="transaction-list",
    ),
    path(
        "admin/<str:pk>/",
        transaction_views.TransactionViewSet.as_view({
            "get": "retrieve",
        }),
        name="transaction-detail",
    ),
]
