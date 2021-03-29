import unittest
import os
import json
from functools import reduce

import context
from src.DataManager import DataManager
from src.OnlineStoreDatabase import OnlineStoreDatabase
from src.Util import getFileContents

def removeLeftOverDbFiles():
    leftOverDB = [path for path in os.listdir() if ".db" in path]
    for dbFile in leftOverDB:
        try:
            os.remove(dbFile)
        except:
            pass

class DataManagerUnitTest(unittest.TestCase):
    """ Tests the DataManager class.
    
        We do alot of querying actual REST APIs here, however this is ok because this is querying
        our testing REST APIs designed to mimic the real APIs the application will call.
        They return predictable data for testing, so there should be no issues.
    """
    dm = None
    testConfig = {
        "databaseFile" : ":memory:",
        "apis" : {
            "Ebay" : {
                "apiRoot" : "http://localhost:5000"
            }
        }
    }
    
    def test_createsConfigWhenNoneExists(self):
        """ The DataManager should create and load a default configuration when it can't find an existing one """
        DataManagerUnitTest.dm.createConfig("testConfigFile.json")
        self.assertTrue(os.path.isfile("testConfigFile.json"))
        os.remove("testConfigFile.json")
            
    def test_addsAllItemsToDatabaseFromConfig(self):
        """ The DataManager should add items to the database from the configured list
        """
        result = DataManagerUnitTest.dm.onlineStoreDatabase.getItems()
        self.assertEqual(len(self.dm.itemList), len(result))
        
    def test_addsListingsFromAPIs(self):
        """ When created, the DataManager should go through all the APIs and add their item listings to the database if they aren't there already
        """
        result = DataManagerUnitTest.dm.onlineStoreDatabase.getListings()
        self.assertEqual(len(DataManagerUnitTest.dm.getAllListings()), len(result))

    def test_addsNewCustomersFromAPIs(self):
        """ When created, the DataManager should go through all the new orders from the APIs and add any new customers to the database
        """
        result = DataManagerUnitTest.dm.onlineStoreDatabase.getCustomers()
        customers = set([key['user']['email'] for key in DataManagerUnitTest.dm.getAllOrders()])
        self.assertEqual(len(customers), len(result))

    def test_addsNewOrdersFromAPIs(self):
        """ When created, the DataManager should go through all the new orders from the APIs and add any new orders to the database
        """
        result = DataManagerUnitTest.dm.onlineStoreDatabase.getOrders()
        self.assertEqual(len(DataManagerUnitTest.dm.getAllOrders()), len(result))

    def test_addsLinkBetweenOrderAndListing(self):
        """ When created, the DataManager should go through all the new orders from the APIs and link them to listings
        """
        result = DataManagerUnitTest.dm.onlineStoreDatabase.getAllOrderListingLinks()
        orders = DataManagerUnitTest.dm.getAllOrders()
        # one link per item in an order, count the number of links expected
        numLinks = reduce(lambda x, y : x + y, [len(x['items']) for x in orders])
        self.assertEqual(numLinks, len(result))
        
    def test_addCustomerAddsACustomer(self):
        """ The addCustomer method should add a customer
        """
        customersBeforeAddingCustomer = DataManagerUnitTest.dm.getCustomers()
        DataManagerUnitTest.dm.addCustomer("John Doe", "johndoe@email.com")
        customersAfterAddingCustomer = DataManagerUnitTest.dm.getCustomers()
        self.assertEqual(1, len(customersAfterAddingCustomer) - len(customersBeforeAddingCustomer))

    def setUp(self):
        removeLeftOverDbFiles()
        DataManagerUnitTest.dm = DataManager(configObj=DataManagerUnitTest.testConfig)
        
    def tearDown(self):
        if os.path.isfile(DataManager.configOverridesFile):
            os.remove(DataManager.configOverridesFile)
        
        del DataManagerUnitTest.dm
        removeLeftOverDbFiles()
    
if __name__ == "__main__":
    unittest.main()