from django.urls import path, include

app_name = "transactions"

urlpatterns = [path("api/v1/", include("transactions.api.v1.urls"))]
