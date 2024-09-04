import uuid
from django.db import models
from django.db import transaction, IntegrityError
from accounts.models.wallet import Wallet
from transactions.models.transactions import Transactions


class Request(models.Model):
    """
    this is a class to define request
    """
    STATUS_CHOICES = (
        ('accept', 'accept'),
        ('reject', 'reject'),
        ('pending', 'pending'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    seller = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    balance = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    @transaction.atomic
    def increase_balance(self):
        try:
            # Check if a transaction with this request already exists
            if Transactions.objects.filter(request=self).exists():
                raise IntegrityError("Transaction with this request already exists.")

            # Update seller wallet balance
            seller_wallet = Wallet.objects.select_for_update().get(user=self.seller)
            seller_wallet.balance += self.balance
            seller_wallet.save()

            # Update status
            request = Request.objects.select_for_update().get(id=self.id)
            request.status = 'accept'
            request.save()
            # Create a transaction record
            Transactions.objects.create(user=self.seller, value=self.balance, request=self)

            return "Records updated successfully"

        except Exception as e:
            # Handle errors, e.g., logging or further exception handling
            raise IntegrityError(f"Update not complete: {str(e)}")
