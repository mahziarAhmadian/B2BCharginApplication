from django_filters import rest_framework as filters
from ...models import Request, Transactions


class RequestFilters(filters.FilterSet):
    class Meta:
        model = Request
        fields = {
            "status": ["exact"],
        }


class TransactionFilters(filters.FilterSet):
    class Meta:
        model = Transactions
        fields = {
            "status": ["exact"],
            "user": ["exact"],
        }
