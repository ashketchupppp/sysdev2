import os.path
import json
from sqlite3.dbapi2 import IntegrityError, OperationalError

import src.Util
from src.OnlineStoreDatabase import OnlineStoreDatabase
from src.StoreAPIs import Ebay

class DataManager:
    """
        Deals with all data processing aspects of the application.
         - Stores the configuration and loads the configuration overrides
         - Creates the database connection
         - Gets all order data from external APIs
    """
    
    configOverridesFile = "configOverrides.json"
    
    defaultConfiguration = {
        "databaseFile" : "onlineStoreDatabase.db",
        "apis" : {
            "Ebay" : {
                "apiRoot" : "http://localhost:5000"
            }
        }
    }

    supportedApis = {
        Ebay.name : Ebay
    }
    
    presetItems = [
        {'stock': 10, 'name': 'Sony Playstation 4', 'location' : 1}, 
        {'stock': 10, 'name': 'Headphones', 'location' : 2}, 
        {'stock': 10, 'name': 'Wireless Mouse', 'location' : 3}, 
        {'stock': 10, 'name': 'Nintendo Switch', 'location' : 4}, 
        {'stock': 10, 'name': 'iPhone 7 Plus', 'location' : 5}, 
        {'stock': 10, 'name': 'Galaxy S9 Edge', 'location' : 6}, 
        {'stock': 10, 'name': 'Laptop', 'location' : 7}, 
        {'stock': 10, 'name': 'Chair', 'location' : 8}, 
        {'stock': 10, 'name': 'Trumpet', 'location' : 9}, 
        {'stock': 10, 'name': 'Plate', 'location' : 10}, 
        {'stock': 10, 'name': 'Mug', 'location' : 11}, 
        {'stock': 10, 'name': 'Door', 'location' : 12}, 
        {'stock': 10, 'name': 'Original Van Gogh', 'location' : 13}, 
        {'stock': 10, 'name': 'Candle', 'location' : 14}
    ]
    
    def __init__(self, configFile=None, configObj=None):
        """ If a config is not passed then attempt to load one from a file, it is then use it.
        """
        if configFile != None:
            if not os.path.isfile(configFile):
                self.createConfig(configFile)
            config = json.loads(src.Util.getFileContents(configFile))
        elif configObj != None:
            config = configObj
        else:
            self.createConfig(DataManager.configOverridesFile)
            config = json.loads(src.Util.getFileContents(DataManager.configOverridesFile))
        self.loadFromConfig(config)
        self.loadDatabase()
        self.createAPIs()

        # go through all the configured APIs and add them to the onlineStore table if we haven't already
        for api in self.apis:
            if not self.onlineStoreDatabase.tableHasRow(OnlineStoreDatabase.storeTable, f'name="{api}"'):
                self.onlineStoreDatabase.insert(OnlineStoreDatabase.storeTable, {"name" : api})

        # add all the items to the database
        for item in DataManager.presetItems:
            try:
                self.onlineStoreDatabase.insert(OnlineStoreDatabase.itemTable, item)
            except OperationalError as e: # if this fails then the item is already there
                pass
        
        self.reload()
        
    # Getting Data
    
    def reload(self):
        """ Queries all configured APIs and updates the internal database with new listings, customers and orders """
        listings = self.getAllListings()
        for listing in listings:
            self.addListing(listing)

        orders = self.getAllOrders()
        for order in orders:
            self.addOrder(order)
    
    def getAllListings(self):
        listings = []
        for api in self.apis:
            listings += self.apis[api].getListings()
        return listings
    
    def getAllOrders(self):
        orders = []
        for api in self.apis:
            orders += self.apis[api].getOrders()
        return orders
    
    # Adding new data
    
    def addOrder(self, orderData):
        # create new customer entries
        self.addCustomer(orderData['user'])

        # create new order entry
        orderColumnValues = {
            "status" : "unprocessed",
            "line1" : orderData['address']['addressLineOne'],
            "line2" : orderData['address']['addressLineTwo'],
            "country" : orderData['address']['country'],
            "streetNameAndNumber" : orderData['address']['streetNameAndNumber'],
            "postcode" : orderData['address']['postcode'],
            "customerEmail" : orderData['user']['email']
        }
        try:
            orderID = self.onlineStoreDatabase.insert(OnlineStoreDatabase.orderTable, orderColumnValues)
        except Exception as e:
            pass
        
        # add links between the order and the listings
        for item in orderData['items']:
            orderListingLinkColumnValues = {
                "orderID" : orderID,
                "storeID" : orderData['storeID'],
                "itemID" : item['name']
            }
            try:
                self.onlineStoreDatabase.insert(OnlineStoreDatabase.orderListingLinkTable, orderListingLinkColumnValues)
            except Exception as e:
                pass
            
    def addCustomer(self, customerData):
        customerColumnValues = {
            'email' : customerData['email'],
            'name' : customerData['name']
        }
        try:
            self.onlineStoreDatabase.insert(OnlineStoreDatabase.customerTable, customerColumnValues)
        except Exception as e:
            pass
    
    def addListing(self, listingData):
        valueDict = {
            'itemID' : listingData['name'],
            'storeID' : listingData['storeID']
        }
        try:
            self.onlineStoreDatabase.insert(OnlineStoreDatabase.listingTable, valueDict)
        except Exception as e:
            pass
        
    # Setup
        
    def loadDatabase(self):
        self.onlineStoreDatabase = OnlineStoreDatabase(self.databaseFile)
    
    def createAPIs(self):
        apiObjs = {}
        for api in self.apis:
            apiObjs[api] = DataManager.supportedApis[api](**self.apis[api])
        self.apis = apiObjs
            
    def createConfig(self, filepath):
        src.Util.writeToFile(filepath, json.dumps(DataManager.defaultConfiguration))
            
    def loadFromConfig(self, configDict):
        """ Load the config from the filepath passed, use defaults if any values are absent from the config file """
        for key in DataManager.defaultConfiguration:
            if not key in self.__dict__:
                setattr(self, key, DataManager.defaultConfiguration[key])
        
        for key in configDict:
            setattr(self, key, configDict[key])