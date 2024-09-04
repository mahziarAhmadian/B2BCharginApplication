from django.urls import path
from ..views import request_views

app_name = "api-v1-request"

urlpatterns = [
    path(
        "seller/get/balance",
        request_views.SellerGetBalanceAPIView.as_view(),
        name="get-balance",
    ),
    path(
        "admin/",
        request_views.RequestViewSet.as_view({
            'get': 'list',
        }),
        name="requests-list",
    ),
    path(
        "admin/<str:pk>/",
        request_views.RequestViewSet.as_view({
            'put': 'update',
        }),
        name="requests-accept",
    ),
]
