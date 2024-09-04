from django_filters import rest_framework as filters
from ...models import Profile


class ProfileFilters(filters.FilterSet):
    """
    valid filter fields arg : exact,iexact,contains,icontains,in,gt,gte,lt,lte,
    startswith,istartswith,endswith

    """

    class Meta:
        model = Profile
        fields = {"first_name": ["in"]}
