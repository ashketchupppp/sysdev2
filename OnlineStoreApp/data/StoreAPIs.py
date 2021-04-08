from abc import ABC, abstractmethod
import json
import asyncio
import functools

from data.Util import doGet, doGetAsync

def apiCall(name):
    """ Decorator for api calls, adds extra information to the result of the API call.
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for i in result:
                i['storeID'] = name
            return result
        return wrapper
    return actual_decorator

class StoreAPI(ABC):
    """
        Abstract class that provides an common interface for getting data from E-Commerce sites APIs.
        All E-Commerce classes must implement this class so that the data from different APIs provide can be accessed
        in a common format.
    """
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
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

    @apiCall(name)
    def getOrders(self):
        orderData = json.loads(doGet(f"{self.apiRoot}/orders"))
        return orderData

    @apiCall(name)
    def getListings(self):
        itemData = json.loads(doGet(f"{self.apiRoot}/listings"))
        return itemData