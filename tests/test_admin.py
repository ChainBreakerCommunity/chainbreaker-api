import unittest
from chainbreaker_api import ChainBreakerClient
from dotenv import dotenv_values
env = dotenv_values(".env")

class TestAdmin(unittest.TestCase):

    ENDPOINT = "http://localhost:8000"

    @classmethod
    def setUpClass(cls):
        cls.client = ChainBreakerClient(TestAdmin.ENDPOINT)
        cls.client.login(env["EMAIL"], env["PASSWORD"])

    def test_get_communities(self):
        communities = self.client.get_communities(country = "canada")
        print(communities)
    
if __name__ == "__main__":
    unittest.main()