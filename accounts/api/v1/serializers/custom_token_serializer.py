from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone_number'] = user.phone_number
        token['is_superuser'] = user.is_superuser
        token['is_seller'] = user.is_seller
        token['is_common_user'] = user.is_common_user
        return token
