import os.path
import json
from tests.Test_OnlineStoreDatabase import OnlineStoreDatabaseUnitTest
import unittest

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
        "Ebay" : Ebay
    }
    
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
        
        # go through all the configured APIs and add them to the database if we haven't already
        for api in self.apis:
            if not self.onlineStoreDatabase.tableHasRow(OnlineStoreDatabase.storeTable, f'name="{api}"'):
                self.onlineStoreDatabase.addStore(api)

        # add all new listings to the database
        for api in self.apis:
            listings = self.apis[api].getListings()
            for listing in listings:
                if not self.onlineStoreDatabase.hasListing(listing['name'], listing['price'], api):
                    self.addListing(listing['name'], 0, listing['price'], api)
        
    # Getting Data
    
    def loadNewOrders(self):
        orders = []
        for api in self.apis:
            orders.append(api.getOrders())
        for order in orders:
            self.onlineStoreDatabase
            
    def addListing(self, name, stock, price, api):
        self.onlineStoreDatabase.addListing(name, price, api, stock)
        
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