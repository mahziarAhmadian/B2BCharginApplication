from django.db.models import Sum
from rest_framework import serializers
from transactions.models import Transactions
from accounts.models.users import User
from accounts.models.wallet import Wallet


class TransferSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    amount = serializers.FloatField()

    class Meta:
        model = Transactions
        fields = ["amount", "phone_number"]

    def validate(self, data):
        phone_number = data.get('phone_number')

        # Check if the common user exists
        try:
            common_user = User.objects.get(phone_number=phone_number, is_common_user=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Common user with this phone number does not exist.")

        data['common_user'] = common_user
        return data

    def create(self, validated_data):
        seller = self.context['request'].user
        common_user = validated_data['common_user']
        amount = validated_data['amount']

        # Call the transaction method
        try:
            Transactions().perform_transfer(seller=seller, common_user=common_user, amount=amount)
            return validated_data
        except Exception as e:
            raise serializers.ValidationError(f"{str(e)}")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    phone_number = serializers.CharField()
    is_seller = serializers.CharField()
    is_common_user = serializers.CharField()
    created_date = serializers.CharField()
    wallet_balance = serializers.SerializerMethodField('get_wallet_balance')

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'is_seller', 'is_common_user', 'wallet_balance', 'created_date']

    def get_wallet_balance(self, obj):
        return Wallet.objects.get(user=obj).balance


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    user = UserSerializer()
    request = serializers.CharField()
    value = serializers.FloatField()
    status = serializers.CharField()
    created_date = serializers.CharField()

    class Meta:
        model = Transactions
        fields = ['id', 'user', 'request', 'value', 'status', 'created_date']

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.method == "GET" and request.parser_context.get(
                "kwargs"
        ).get("pk"):
            total_transaction_amounts = Transactions.objects.filter(user=rep['user']['id']).aggregate(Sum('value'))
            rep['user']['total_transaction_amounts'] = total_transaction_amounts['value__sum']
        return rep
