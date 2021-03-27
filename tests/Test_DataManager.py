import unittest
import os
import json

import context
from src.DataManager import DataManager
from src.OnlineStoreDatabase import OnlineStoreDatabase
from src.Util import getFileContents

class DataManagerUnitTest(unittest.TestCase):
    dm = None
    
    def test_createsConfigWhenNoneExists(self):
        """ The DataManager should create and load a default configuration when it can't find an existing one """
        self.assertTrue(os.path.isfile(DataManager.configOverridesFile))
        
        for key in DataManager.defaultConfiguration:
            self.assertIn(key, DataManagerUnitTest.dm.__dict__)
        
    def setUp(self):
        DataManagerUnitTest.dm = DataManager()
        
    def tearDown(self):
        if os.path.isfile(DataManager.configOverridesFile):
            os.remove(DataManager.configOverridesFile)
        
        if os.path.isfile(DataManagerUnitTest.dm.databaseFile):
            DataManagerUnitTest.dm.onlineStoreDatabase.close()
            os.remove(DataManagerUnitTest.dm.databaseFile)
            
        DataManagerUnitTest.dm = None
        
    
if __name__ == "__main__":
    unittest.main()