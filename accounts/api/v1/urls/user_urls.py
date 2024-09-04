from django.urls import path

from ..views import user_views

app_name = "api-v1"
urlpatterns = [
    path(
        "login/", user_views.UserLoginGenericAPIView.as_view(), name="login"
    ),
    path(
        "seller/user/", user_views.SellerGetUserAPIView.as_view(), name="get-user"
    ),
]
