import unittest

import context

from src.StoreAPIs import *
from src.DataManager import DataManager

class StoreAPIsUnitTest(unittest.TestCase):
    def test_getOrders(self):
        pass
        """
            Tests all subclasses of the StoreAPI class, ensures their getOrders method returns data in the correct format.
            StoreAPI is an abstract class and so could be used to implement many different APIs which would all return
            different data. The implementors of this class must all process that data and return it in a common format.
        """
#        schema = {
#            "name" : "",
#            "email" : "",
#            "addressLineOne" : "",
#            "addressLineTwo" : "",
#            "country" : "",
#            "streetNameAndNumber" : "",
#            "postcode" : "",
#            "store" : "",
#            "items" : [
#                {
#                    "name" : "",
#                    "price" : ""
#                }
#            ]
#        }
#        
#        for StoreAPIImplementer in list(StoreAPI.__subclasses__()):
#            APIInstance = StoreAPIImplementer()
#            orders = APIInstance.getOrders()
#            for order in orders:
#                results = [(key, key in order) for key in list(schema.keys())]
#                for result in results:
#                    if not result[1]:
#                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.__name__}")
#                
#                results = [(key, key in order["items"]) for key in list(schema["items"].keys())]
#                for result in results:
#                    if not result[1]:
#                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.__name__}")

if __name__ == "__main__":
    unittest.main()