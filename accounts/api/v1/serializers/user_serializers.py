from django.conf import settings
from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.api.v1.serializers.custom_token_serializer import CustomTokenObtainPairSerializer

class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        required=True, write_only=True
    )

    access = serializers.CharField(allow_blank=True, read_only=True)

    refresh = serializers.CharField(allow_blank=True, read_only=True)

    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    class Meta(object):
        model = User
        fields = [
            "phone_number",
            "password",
            "access",
            "refresh",
        ]

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        username = data.get("username", None)
        password = data.get("password", None)

        if not phone_number and not username:
            raise serializers.ValidationError(
                "Please enter username or phone_number to login."
            )

        user = (
            User.objects.filter(phone_number=phone_number)
            .exclude(phone_number__isnull=True)
            .exclude(phone_number__iexact="")
            .distinct()
        )

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError(
                "This username/phone_number is not valid."
            )

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            # Generate tokens using the custom serializer
            custom_serializer = CustomTokenObtainPairSerializer()
            token = custom_serializer.get_token(user_obj)
            # token = self.get_tokens_for_user(user=user_obj)
            data['access'] = str(token.access_token)
            data['refresh'] = str(token)
        else:
            raise serializers.ValidationError("User not active.")
        return data
class SellerGetUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    phone_number = serializers.CharField()
    is_common_user = serializers.BooleanField()
    created_date = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'is_common_user', 'created_date']
