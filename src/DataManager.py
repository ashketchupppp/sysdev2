import os.path
import json
from tests.Test_OnlineStoreDatabase import OnlineStoreDatabaseUnitTest
import unittest

import src.Util
from src.OnlineStoreDatabase import OnlineStoreDatabase

class DataManager:
    """
        Deals with all data processing aspects of the application.
         - Stores the configuration and loads the configuration overrides
         - Creates the database connection
         - Gets all order data from external APIs
    """
    
    configOverridesFile = "configOverrides.json"
    
    defaultConfiguration = {
        "databaseFile" : "onlineStoreDatabase.db"
    }
    
    def __init__(self):
        if not os.path.isfile(DataManager.configOverridesFile):
            self.createConfig(DataManager.configOverridesFile)
        self.loadFromConfig(DataManager.configOverridesFile)
        self.loadDatabase()
        
    def loadDatabase(self):
        self.onlineStoreDatabase = OnlineStoreDatabase(self.databaseFile)
            
    def createConfig(self, filepath):
        src.Util.writeToFile(filepath, json.dumps(DataManager.defaultConfiguration))
            
    def loadFromConfig(self, filepath):
        """ Load the config from the filepath passed, use defaults if any values are absent from the config file """
        for key in DataManager.defaultConfiguration:
            if not key in self.__dict__:
                setattr(self, key, DataManager.defaultConfiguration[key])
        
        config = json.loads(src.Util.getFileContents(filepath))
        for key in config:
            setattr(self, key, config[key])