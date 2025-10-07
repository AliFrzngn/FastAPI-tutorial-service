from locust import HttpUser, task, between


class QuickStartUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        response = self.client.post("/users/login", json={
            "username": "hiborat", "password": "Hiboratune.99"
            })
        access_token = response.json()["access_token"]
        self.client.headers = {'Authorization': f'Bearer {access_token}'}

    @task
    def initial_task(self):
        self.client.get("/initiate-task")
    
    
    @task
    def task_list(self):
        self.client.get("/todo/task")

    @task
    def not_found(self):
        self.client.get("/not-found")

    @task
    def fetch_current_weather(self):
        self.client.get("/fetch-current-weather")