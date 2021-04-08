import os.path
import json

from data.Util import *
from data.OnlineStoreDatabase import OnlineStoreDatabase
from data.StoreAPIs import Ebay

class DataManager:
    """
        This is the "integrator" class of the data module,  it deals with all data processing aspects of the application.
         - Stores the default configuration
         - Loading the configuration overrides
         - Creating the OnlineStoreDatabase and providing instance methods to interface with the database
         - Setting up the API class instances
         - Providing methods for interfacing with all the APIs
    """

    rootDir = os.path.abspath(os.path.join(os.path.join(os.path.realpath(__file__), os.path.pardir), os.path.pardir))
    configOverridesFile = f"{rootDir}\\configOverrides.json"
    
    defaultConfiguration = {
        "databaseFile" : f"{rootDir}\\onlineStoreDatabase.db",
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
            "orderUpdatePassword" : "outfiurfkimfri" # need to figure out a way of NOT storing passwords in plaintext, I typed randomly for this password it means nothing
        }
    }

    supportedApis = {
        Ebay.name : Ebay
    }
    
    def __init__(self, configFile=None, configObj=None):
        """ Class constructor.
            
            If a configFile (str) is passed then it is read as a JSON file and loaded as the config
            If no configFile is passed then one with default values is created at the root of the application, read as a JSON file and loaded as the config
            If a configObj (dict) is passed then it is loaded as the config and no configFile is written 
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
    
    async def printAddressLabel(self, orderID, outputFile):
        """ Writes an address label for the passed order into the passed outputFile
        """
        order = await self.onlineStoreDatabase.getOrder(orderID)
        customer = await self.onlineStoreDatabase.getCustomer(order['email'])
        label = f"""{customer['name']}
{order['streetNameAndNumber']}
{order['line1']}
{order['line2']}
{order['postcode']}
{order['country']}"""
        writeToFile(outputFile, label)
        
    # Getting Data
    
    async def reload(self):
        """ Queries all configured APIs and updates the internal database with new listings, customers and orders 
            Any orders with id fields that are already in the database will not be added.
        """
        listings = await self.getApiListings()
        for listing in listings:
            self.onlineStoreDatabase.addListing(itemID=listing['name'], storeID=listing['storeID'], price=listing['price'])

        orders = await self.getApiOrders()
        for order in orders:
            self.onlineStoreDatabase.addOrder(order)
    
    async def getApiListings(self):
        """ Queries all configured APIs for listings and compiles the results into a single list
        """
        listings = []
        for api in self.apis:
            listings += self.apis[api].getListings()
        return listings
    
    async def getApiOrders(self):
        """ Queries all configured APIs for orders and compiles the results into a single list
        """
        orders = []
        for api in self.apis:
            orders += self.apis[api].getOrders()
        return orders
    
    # Stored Data
    
    async def getUnprocessedOrders(self, asDict=False):
        """ Queries the OnlineStoreDatabase for a list of orders that are marked as "unprocessed"
        """
        if asDict:
            return [dict(row) for row in self.onlineStoreDatabase.getUnprocessedOrders()]
        else:
            return self.onlineStoreDatabase.getUnprocessedOrders()
    
    async def getOrderPackingList(self, orderID):
        """ Queries the OnlineStoreDatabase for a list of items in an order
        """
        return self.onlineStoreDatabase.getOrderPackingList(orderID)
    
    async def getAllOrderListingLinks(self):
        """ Queries the OnlineStoreDatabase for all entries in the orderListingLink table
        """
        return self.onlineStoreDatabase.getAllOrderListingLinks()
    
    async def getOrders(self):
        return self.onlineStoreDatabase.getOrders()

    async def getListings(self):
        return self.onlineStoreDatabase.getListings()
    
    async def getItems(self):
        return self.onlineStoreDatabase.getItems()
    
    async def getCustomers(self):
        return self.onlineStoreDatabase.getCustomers()
    
    async def getCustomer(self, email):
        return self.onlineStoreDatabase.getCustomer(email)
    
    async def getOrder(self, orderID):
        return self.onlineStoreDatabase.getOrder(orderID)

    # Adding new data
    
    async def addOrder(self, orderData):
        return self.onlineStoreDatabase.addOrder(orderData)
            
    async def addCustomer(self, name, email):
        return self.onlineStoreDatabase.addCustomer(name, email)
    
    async def addListing(self, itemID, storeID, price):
        return self.onlineStoreDatabase.addListing(itemID, storeID, price)
        
    # Setup
        
    def loadDatabase(self):
        """ Creates the onlineStoreDatabase file.
            Anything that needs to be done before or after creating this needs to be put here.
        """
        self.onlineStoreDatabase = OnlineStoreDatabase(self.databaseFile)
    
    def createAPIs(self):
        """ Goes through the self.apis variable (which is gotten from the configuration) and creates all configured API objects.
            When each API object is instantiated it is passed its unpacked dictionary loaded from the configuration.
            If an API is configured but not listed in DataManager.supportedApis it will not be loaded.
        """
        apiObjs = {}
        for api in self.apis:
            if api in DataManager.supportedApis:
                apiObjs[api] = DataManager.supportedApis[api](**self.apis[api])
        self.apis = apiObjs
            
    def createConfig(self, filepath):
        writeToFile(filepath, json.dumps(dict(DataManager.defaultConfiguration)))
            
    def loadFromConfig(self, configDict):
        """ Load the config from the filepath passed, use defaults if any values are absent from the config file
        """
        for key in DataManager.defaultConfiguration:
            if not key in self.__dict__:
                setattr(self, key, DataManager.defaultConfiguration[key])
        
        for key in configDict:
            setattr(self, key, configDict[key])