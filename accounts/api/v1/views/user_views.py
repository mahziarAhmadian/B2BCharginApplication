from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import user_serializers

User = get_user_model()


class UserLoginGenericAPIView(generics.GenericAPIView):
    """
    Endpoint for user login. Returns authentication token on success.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerGetUserAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = user_serializers.SellerGetUserSerializer
    queryset = User.objects.filter(is_common_user=True)
