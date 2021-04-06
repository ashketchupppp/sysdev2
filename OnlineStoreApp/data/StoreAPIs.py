from abc import ABC, abstractmethod
import json
import asyncio

from data.Util import doGet

class StoreAPI(ABC):
    """
        Abstract class that provides an common interface for getting data from E-Commerce sites APIs.
        All E-Commerce classes must implement this class so that the data from different APIs provide can be accessed
        in a common format.
    """
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def apiCall(self, apiCallFunction):
        def wrapper():
            result = apiCallFunction()
            for i in result:
                i['storeID'] = self.name
            return result
        return wrapper
    
    @abstractmethod
    def getOrders(self):
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
                    "listings" : [
                        {
                            "name" : "",
                            "price" : ""
                        }
                    ]
                }
            ]
            It is up to the implementer of this class to process the data and put it into this structure.
        """
        pass
    
    @abstractmethod
    def getListings(self):
        """
            To be overriden by a class implementing StoreAPI.
            Must return a list of dictionaries with the following structure:
            [
                {
                    "name" : "",
                    "price" : "",
                    "storeID" : ""
                }
            ]
            It is up to the implementer of this class to process the data and put it into this structure.
        """

    
class Ebay(StoreAPI):
    defaultConfiguration = {
        'apiRoot' : 'http://localhost:5000'
    }
    name = 'Ebay'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # if there are any config values not provided, use the defaults
        for configKey in Ebay.defaultConfiguration:
            if not configKey in self.__dict__:
                setattr(self, configKey, Ebay.defaultConfiguration[configKey])

    def getOrders(self):
        orderData = json.loads(doGet(f"{self.apiRoot}/orders"))
        # orderData = json.loads(doGet(f"{self.apiRoot}/orders"))
        for order in orderData:
            order['storeID'] = Ebay.name
        return orderData
    
    def getListings(self):
        itemData = json.loads(doGet(f"{self.apiRoot}/listings"))
        # itemData = json.loads(doGet(f"{self.apiRoot}/listings"))
        for item in itemData:
            item['storeID'] = Ebay.name
        return itemData