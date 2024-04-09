import unittest
from fastapi.testclient import TestClient
from app.routers.health_check import router

class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status_code": 200,
            "detail": "ok",
            "result": "working"
        })