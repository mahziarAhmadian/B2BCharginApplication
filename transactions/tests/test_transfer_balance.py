import random
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Wallet
from transactions.models import Request, Transactions
from django.db.models import Sum


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user_obj = User.objects.create_user(
        phone_number="09121236547", password="1234"
    )
    return user_obj


@pytest.fixture
def super_admin():
    user_obj = User.objects.create_superuser(
        phone_number="09122222222", password="1234"
    )
    return user_obj


@pytest.fixture
def seller1():
    user_obj = User.objects.create_seller(
        phone_number="09125555555", password="1234"
    )
    return user_obj


@pytest.fixture
def seller2():
    user_obj = User.objects.create_seller(
        phone_number="09125555554", password="1234"
    )
    return user_obj


@pytest.mark.django_db
class TestTransactionApi:
    @pytest.mark.parametrize("amount", [1000000, 2000000])
    def create_and_approve_balance(self, api_client, seller, super_admin, amount=1000000):
        """Helper function to create and approve a balance request for a seller."""
        # Create balance request
        api_client.force_authenticate(user=seller)
        url = reverse("transactions:api-v1-request:get-balance")
        data = {"balance": amount}
        response = api_client.post(url, data)
        assert response.status_code == 201
        # Approve balance request by admin
        request_id = Request.objects.get(seller=seller, status='pending', balance=data.get('balance')).id
        api_client.force_authenticate(user=super_admin)
        url = reverse("transactions:api-v1-request:requests-accept", kwargs={'pk': request_id})
        data = {"status": "accept"}
        response = api_client.put(url, data)
        assert response.status_code == 200

        return seller.wallet.balance

    def perform_transfer(self, api_client, seller, common_user, amount):
        """Helper function to perform a balance transfer."""
        api_client.force_authenticate(user=seller)
        url = reverse("transactions:api-v1-transaction:sell")
        data = {
            "phone_number": common_user.phone_number,
            "amount": amount
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def verify_balance(self, seller):
        """Helper function to verify if the seller's wallet balance matches the sum of their transactions."""
        seller_balance = Wallet.objects.get(user=seller).balance
        transactions_balance = Transactions.objects.filter(user=seller).aggregate(Sum('value'))['value__sum']
        assert seller_balance == transactions_balance, (
            f"Balance mismatch: Wallet balance is {seller_balance}, "
            f"but transactions sum is {transactions_balance}."
        )

    @pytest.fixture
    def setup_sellers_with_balance(self, api_client, seller1, seller2, super_admin):
        """Fixture to set up sellers with an initial approved balance."""
        sellers = [seller1, seller2]
        for seller in sellers:
            for _ in range(10):
                self.create_and_approve_balance(api_client, seller, super_admin)
        return sellers

    @pytest.mark.parametrize("amount", [10, 20, 50, 100, 200])  # Example amounts
    def test_multiple_transfers_and_balance_verification(self, api_client, setup_sellers_with_balance, common_user,
                                                         amount):
        """Test multiple transfers for two sellers and verify balance integrity."""
        sellers = setup_sellers_with_balance

        for seller in sellers:
            for _ in range(1000):  # Perform 1000 transfers
                self.perform_transfer(api_client, seller, common_user, amount)

            # Verify the seller's balance matches the sum of their transactions
            self.verify_balance(seller)
