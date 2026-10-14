import unittest

from app import app


class TestFineEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fine_is_returned_as_json(self):
        response = self.client.get("/fine?days=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["fee"], 1.50)

    def test_deluxe_flag_reaches_the_fee_calculation(self):
        response = self.client.get("/fine?days=5&deluxe=1")
        self.assertEqual(response.get_json()["fee"], 3.00)

    def test_non_numeric_days_is_a_400_not_a_crash(self):
        response = self.client.get("/fine?days=abc")
        self.assertEqual(response.status_code, 400)

    def test_negative_days_is_a_400_not_a_crash(self):
        response = self.client.get("/fine?days=-1")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
