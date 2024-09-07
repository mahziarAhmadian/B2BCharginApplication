from rest_framework import serializers
from transactions.models.request import Request


class SellerRequestSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField()

    class Meta:
        model = Request
        fields = ["balance"]

    def validate_balance(self, balance):
        return balance


class RequestSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    seller = serializers.CharField(read_only=True)
    status = serializers.CharField()
    created_date = serializers.CharField(read_only=True)
    balance = serializers.FloatField(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'seller', 'status', 'created_date', 'balance']

    def validate_status(self, status):
        validate_status = ['accept', 'reject', 'pending']
        if status not in validate_status:
            raise serializers.ValidationError("status not valid.")
        return status
