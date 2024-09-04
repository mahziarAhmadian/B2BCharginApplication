from django.urls import path, include

urlpatterns = [
    path("request/", include("transactions.api.v1.urls.request_urls")),
    path("", include("transactions.api.v1.urls.transaction_urls")),
    # path("category/", include("blog.api.v1.urls.category_urls")),
]
