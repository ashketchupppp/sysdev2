import os.path
import json
from sqlite3.dbapi2 import IntegrityError, OperationalError
import asyncio

from data.Util import *
from data.OnlineStoreDatabase import OnlineStoreDatabase
from data.StoreAPIs import Ebay
from data.Email import EmailHandler

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
        },
        "itemList" : [
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
        ],
        "email" : {
            "orderUpdateEmail" : "company@noreply.com",
            "orderUpdatePassword" : "outfiurfkimfri" # need to figure out a way of NOT storing passwords in plaintext
        }
    }

    supportedApis = {
        Ebay.name : Ebay
    }
    
    def __init__(self, configFile=None, configObj=None):
        """ If a config is not passed then attempt to load one from a file
        """
        if configFile != None:
            if not os.path.isfile(configFile):
                self.createConfig(configFile)
            config = json.loads(getFileContents(configFile))
        elif configObj != None:
            config = configObj
        else:
            self.createConfig(DataManager.configOverridesFile)
            config = json.loads(getFileContents(DataManager.configOverridesFile))
        self.loadFromConfig(config)
        self.loadDatabase()
        self.createAPIs()
        
        # create the email handler (broken)
        # self.emailHandler = EmailHandler(self.email['orderUpdateEmail'], self.email['orderUpdatePassword'])

        # go through all the configured APIs and add them to the onlineStore table if we haven't already
        for api in self.apis:
            self.onlineStoreDatabase.addOnlineStore(api)

        # add all the items to the database
        for item in self.itemList:
            self.onlineStoreDatabase.addItem(name=item['name'], stock=item['stock'], location=item['location'])
        
    # Address Labels
    
    def printAddressLabel(self, orderID, outputFile):
        order = self.onlineStoreDatabase.getOrder(orderID)
        customer = self.onlineStoreDatabase.getCustomer(order['email'])
        label = f"""{customer['name']}
{order['streetNameAndNumber']}
{order['line1']}
{order['line2']}
{order['postcode']}
{order['country']}"""
        writeToFile(outputFile, label)
        
    # Getting Data
    
    def reload(self):
        """ Queries all configured APIs and updates the internal database with new listings, customers and orders """
        listings = self.getAllListings()
        for listing in listings:
            self.onlineStoreDatabase.addListing(itemID=listing['name'], storeID=listing['storeID'], price=listing['price'])

        orders = self.getAllOrders()
        for order in orders:
            self.onlineStoreDatabase.addOrder(order)
    
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
    
    # Stored Data

    
    def getUnprocessedOrders(self, asDict=False):
        if asDict:
            return [dict(row) for row in self.onlineStoreDatabase.getUnprocessedOrders()]
        else:
            return self.onlineStoreDatabase.getUnprocessedOrders()
    
    def getOrderPackingList(self, orderID):
        return self.onlineStoreDatabase.getOrderPackingList(orderID)
    
    def getAllOrderListingLinks(self):
        return self.onlineStoreDatabase.getAllOrderListingLinks()
    
    def getOrders(self):
        return self.onlineStoreDatabase.getOrders()
    
    def getItems(self):
        return self.onlineStoreDatabase.getItems()
    
    def getCustomers(self):
        return self.onlineStoreDatabase.getCustomers()
    
    def getOrder(self, orderID):
        return self.onlineStoreDatabase.getOrder(orderID)

    # Adding new data
    
    def addOrder(self, orderData):
        return self.onlineStoreDatabase.addOrder(orderData)
            
    def addCustomer(self, name, email):
        return self.onlineStoreDatabase.addCustomer(name, email)
    
    def addListing(self, itemID, storeID, price):
        return self.onlineStoreDatabase.addListing(itemID, storeID, price)
        
    # Setup
        
    def loadDatabase(self):
        self.onlineStoreDatabase = OnlineStoreDatabase(self.databaseFile)
    
    def createAPIs(self):
        apiObjs = {}
        for api in self.apis:
            apiObjs[api] = DataManager.supportedApis[api](**self.apis[api])
        self.apis = apiObjs
            
    def createConfig(self, filepath):
        writeToFile(filepath, json.dumps(dict(DataManager.defaultConfiguration)))
            
    def loadFromConfig(self, configDict):
        """ Load the config from the filepath passed, use defaults if any values are absent from the config file """
        for key in DataManager.defaultConfiguration:
            if not key in self.__dict__:
                setattr(self, key, DataManager.defaultConfiguration[key])
        
        for key in configDict:
            setattr(self, key, configDict[key])