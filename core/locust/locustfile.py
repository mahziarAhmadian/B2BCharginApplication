import random
from locust import HttpUser, task, between



class Seller(HttpUser):
    wait_time = between(1, 2)  # Wait 1 to 2 seconds between task cycles

    def seller_login(self):
        """
                Perform login and get an access token when a user starts.
                """
        credentials = [
            {"phone_number": "09121234567", "password": "1234"},
            {"phone_number": "09121234598", "password": "1234"},
            {"phone_number": "09121634598", "password": "1234"}
        ]

        # Randomly assign credentials to the user
        self.user_credentials = random.choice(credentials)

        # Perform the login
        response = self.client.post("/accounts/api/v1/login/", json=self.user_credentials)

        # Extract the access token from the response
        return response.json().get("access")

    def seller_get_balance_request(self):
        # send request to get balance
        headers = {
            "Authorization": f"Bearer {self.token}"  # Include the access token in the headers
        }
        self.client.post("/transactions/api/v1/request/seller/get/balance", json={
            "balance": 1000000,
        }, headers=headers)

    def admin_accept_balance(self):
        # admin accept balance request
        admin_response = self.client.post("/accounts/api/v1/login/", json={
            "phone_number": "09351234567",
            "password": "1234"
        })
        self.admin_token = admin_response.json().get("access")
        # get request by admin
        admin_headers = {
            "Authorization": f"Bearer {self.admin_token}"
        }
        seller_request = self.client.get("/transactions/api/v1/request/admin/", params={
            "status": "pending",
            "seller__phone_number": self.user_credentials.get('phone_number'),
        }, headers=admin_headers)
        request_id = seller_request.json()[0].get("id")
        # accept request
        self.client.put(f"/transactions/api/v1/request/admin/{request_id}/", json={"status": "accept"},
                        headers=admin_headers)

    def on_start(self):
        self.token = self.seller_login()
        if not self.token:
            raise Exception("No token found in login response")
        self.seller_get_balance_request()
        self.admin_accept_balance()

    @task
    def sell_balance(self):
        """
        Simulate a seller making a sale by sending a POST request to the /seller/sell endpoint.
        """
        headers = {
            "Authorization": f"Bearer {self.token}"  # Include the access token in the headers
        }
        amount = [100, 200, 300, 50, 45, 75, 10]
        self.client.post("/transactions/api/v1/seller/sell", json={
            "phone_number": "09356165600",
            "amount": random.choice(amount)
        }, headers=headers)
