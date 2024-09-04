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


@pytest.mark.django_db
class TestTransactionApi:
    def test_get_balance_request_response_status_201(self, api_client, seller1):
        api_client.force_authenticate(user=seller1)
        url = reverse("transactions:api-v1-request:get-balance")
        data = {
            "balance": 1000000
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_admin_accept_balance_request_status_200(self, api_client, seller1, super_admin):
        # create get balance request with seller
        api_client.force_authenticate(user=seller1)
        url = reverse("transactions:api-v1-request:get-balance")
        data = {
            "balance": 1000000
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        # get request_id
        request_id = Request.objects.get(seller=seller1, status='pending', balance=data.get('balance')).id
        # accept balance with admin
        api_client.force_authenticate(user=super_admin)
        url = reverse("transactions:api-v1-request:requests-accept", kwargs={'pk': request_id})
        data = {
            "status": "accept"
        }
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_seller_transfer_balance_status_201(self, api_client, seller1, common_user, super_admin):
        # create get balance request with seller1
        api_client.force_authenticate(user=seller1)
        url = reverse("transactions:api-v1-request:get-balance")
        data = {
            "balance": 1000000
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        # get seller1 request_id
        request_id = Request.objects.get(seller=seller1, status='pending', balance=data.get('balance')).id
        # accept balance for seller1 with admin
        api_client.force_authenticate(user=super_admin)
        url = reverse("transactions:api-v1-request:requests-accept", kwargs={'pk': request_id})
        data = {
            "status": "accept"
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        # transfer balance from seller to common user
        user_phone_number = common_user.phone_number
        api_client.force_authenticate(user=seller1)
        url = reverse("transactions:api-v1-transaction:sell")
        data = {
            "phone_number": user_phone_number,
            "amount": 100
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        # check transaction balance with correct balance
        seller_balance = Wallet.objects.get(user=seller1).balance
        transactions_balance = Transactions.objects.filter(user=seller1).aggregate(Sum('value'))['value__sum']
        assert seller_balance == transactions_balance, (
            f"Balance mismatch: Wallet balance is {seller_balance}, "
            f"but transactions sum is {transactions_balance}."
        )
