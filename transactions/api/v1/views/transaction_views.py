from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.transaction_serializer import TransferSerializer, TransactionSerializer
from transactions.api.v1.permission import IsSuperAdmin, IsSeller
from rest_framework.response import Response
from transactions.models import Transactions
from transactions.api.v1.filters import TransactionFilters
from transactions.api.v1.paginations import CustomPagination


class TransferAPIView(generics.CreateAPIView):
    permission_classes = [IsSeller]
    serializer_class = TransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperAdmin]
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilters
    ordering_fields = ["created_date"]
    pagination_class = CustomPagination
