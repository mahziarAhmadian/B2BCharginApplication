import uuid
from django.db import models
from django.db import transaction, IntegrityError
from accounts.models.users import User
from accounts.models.wallet import Wallet


class Transactions(models.Model):
    """
    this is a class to define categories for blog table
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey('transactions.Request', on_delete=models.CASCADE, null=True)
    value = models.FloatField()
    status = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        if self.value > 0:
            self.status = 'increase'
        else:
            self.status = 'decrease'
        super(Transactions, self).save(*args, **kwargs)

    @transaction.atomic
    def perform_transfer(self, seller, common_user, amount):
        try:
            seller_wallet = Wallet.objects.select_for_update().get(user=seller)
            if seller_wallet.balance < amount:
                raise ValueError("Insufficient balance in seller's wallet.")

            # Decrease balance from seller's wallet
            seller_wallet.balance -= amount
            seller_wallet.save()

            # Increase balance to common user's wallet
            common_user_wallet = Wallet.objects.select_for_update().get(user=common_user)
            common_user_wallet.balance += amount
            common_user_wallet.save()
            # Log the transaction for the seller (decrease)
            Transactions.objects.create(
                user=seller,
                request=None,
                value=-amount,
                status='decrease'
            )
            # Log the transaction for the common user (increase)
            Transactions.objects.create(
                user=common_user,
                request=None,
                value=amount,
                status='increase'
            )

            return "Transfer completed"

        except Exception as e:
            # Handle errors, e.g., logging or further exception handling
            raise IntegrityError(f"Transfer fail: {str(e)}")
