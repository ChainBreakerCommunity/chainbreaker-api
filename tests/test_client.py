import unittest
from chainbreaker_api import ChainBreakerClient
from dotenv import dotenv_values
env = dotenv_values(".env")

class TestClient(unittest.TestCase):

    ENDPOINT = "http://localhost:8000"

    @classmethod
    def setUpClass(cls):
        cls.client = ChainBreakerClient(TestClient.ENDPOINT)
        cls.client.login(env["EMAIL"], env["PASSWORD"])
        
    def test_status(self):
        res = self.client.get_status()
        print(res)

if __name__ == "__main__":
    unittest.main()