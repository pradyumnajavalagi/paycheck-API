# locustfile.py
from locust import HttpUser, task, between

class PayCheckUser(HttpUser):
    # Each simulated user will wait 1 to 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """Called when a Locust start before any task is scheduled."""
        # --- Log in and get an auth token for this user ---
        # For a real test, you'd use a pool of users. Here we'll use one.
        response = self.client.post("/login", data={"username": "user_1", "password": "pass123"})
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            print("Failed to login and get token.")

    @task
    def get_own_bills(self):
        """Simulates a user fetching their own due bills."""
        if hasattr(self, 'headers'):
            self.client.get("/bills/user_1", headers=self.headers, name="/bills/{user_id}")

    @task
    def get_own_transactions(self):
        """Simulates a user fetching their transaction history."""
        if hasattr(self, 'headers'):
            self.client.get("/transactions/user_1", headers=self.headers, name="/transactions/{user_id}")