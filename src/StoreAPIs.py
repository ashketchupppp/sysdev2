from abc import ABC, abstractmethod

class StoreAPI(ABC):
    """
        Abstract class that provides an common interface for getting data from E-Commerce sites APIs.
        All E-Commerce classes must implement this class so that the data different APIs provide can be accessed
        in a common format.
    """
    
    @abstractmethod
    def getOrders(self) -> list:
        """
            To be overridden by a class implementing StoreAPI.
            Must return a list of dictionaries with the following structure:
            [
                {
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
            ]
        """
        pass
    
class EbayAPI(StoreAPI):
    def __init__(self):
        pass
    
    def getOrders(self):
        return {"awd" : 0}