from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from transactions.api.v1.filters import RequestFilters

from transactions.models import Request
from ..permission import IsSeller, IsSuperAdmin
from ..serializers.request_serializers import SellerRequestSerializer, RequestSerializer
from rest_framework.response import Response
from django.db import IntegrityError


class SellerGetBalanceAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    serializer_class = SellerRequestSerializer
    queryset = Request.objects.all()

    def create(self, request, *args, **kwargs):
        if Request.objects.filter(seller=request.user, status='pending').exists():
            return Response('you have one request on pending', status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            balance = serializer.validated_data.get('balance')
            Request.objects.create(seller=request.user, balance=balance)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RequestFilters
    ordering_fields = ["created_date"]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)  # Use partial=True if only a few fields are being updated
        if serializer.is_valid(raise_exception=True):
            validate_status = serializer.validated_data.get('status')

            if validate_status == 'accept':
                try:
                    # Attempt to increase the balance
                    instance.increase_balance()
                    return Response("Update successfully", status=status.HTTP_200_OK)
                except IntegrityError as e:
                    # Handle any integrity errors (like duplicate transactions)
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    # Handle any other unforeseen errors
                    return Response({"detail": "An error occurred: " + str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                # If the status is not 'accept', just save the changes (if any)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
