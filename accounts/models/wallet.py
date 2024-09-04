import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .users import User


class Wallet(models.Model):
    """
    Profile class for each user which is being created to hold the information
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Wallet"

    def __str__(self):
        return f"{self.id}"


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal for post creating a wallet which activates when a user being created ONLY
    """
    if created:
        if instance.is_seller or instance.is_common_user:
            Wallet.objects.create(user=instance)
