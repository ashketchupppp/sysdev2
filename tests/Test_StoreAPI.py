import unittest

import context

from src.StoreAPIs import *

class StoreAPIsUnitTest(unittest.TestCase):
    def test_getOrders(self):
        """
            Tests all subclasses of the StoreAPI class, ensures their getOrders method returns data in the correct format.
        """
        schema = {
            "name" : "",
            "email" : "",
            "addressLineOne" : "",
            "addressLineTwo" : "",
            "country" : "",
            "streetNameAndNumber" : "",
            "postcode" : "",
            "items" : [
                {
                    "name" : "",
                    "price" : ""
                }
            ]
        }
        for StoreAPIImplementer in list(StoreAPI.__subclasses__()):
            APIInstance = StoreAPIImplementer()
            orders = APIInstance.getOrders()
            for order in orders:
                results = [(key, key in order) for key in list(schema.keys())]
                for result in results:
                    if not result[1]:
                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.__name__}")
                
                results = [(key, key in order["items"]) for key in list(schema["items"].keys())]
                for result in results:
                    if not result[1]:
                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.__name__}")

if __name__ == "__main__":
    unittest.main()