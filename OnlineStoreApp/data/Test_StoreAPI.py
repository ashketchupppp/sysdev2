import unittest



from data.StoreAPIs import *
from data.DataManager import DataManager

class StoreAPIsUnitTest(unittest.TestCase):
    def test_getOrders(self):
        """ Although this test is a good idea, I haven't managed to figure out the problem of setting up fake APIs for testing.
            For each new API we implement, we need a way of getting fake data for testing.
        """
        pass
#        """
#            Tests all subclasses of the StoreAPI class, ensures their getOrders method returns data in the correct format.
#            StoreAPI is an abstract class and so could be used to implement many different APIs which would all return
#            different data. The implementors of this class must all process that data and return it in a common format.
#        """
#        schema = {
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
#                        print(result)
#                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.name}")
#                
#                results = [(key, key in order["items"]) for key in list(schema["items"].keys())]
#                for result in results:
#                    if not result[1]:
#                        self.fail(f"{result[0]} incorrect for {StoreAPIImplementer.name}")
                        
if __name__ == "__main__":
   unittest.main()