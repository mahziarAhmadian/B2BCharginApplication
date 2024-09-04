from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api-v1-tokens"
urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
