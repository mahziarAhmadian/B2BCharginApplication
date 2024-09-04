from django.urls import path, include

urlpatterns = [
    path("", include("accounts.api.v1.urls.user_urls")),
    # path("profile/", include("accounts.api.v1.urls.profile_urls")),
    path("jwt/", include("accounts.api.v1.urls.jwt_urls")),
]
