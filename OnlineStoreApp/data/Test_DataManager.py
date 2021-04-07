import unittest
import os
from functools import reduce
import threading
import asyncio

from data.DataManager import DataManager
from data.webay import runWebay

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
    webayThread = None
    webayHost = "127.0.0.1"
    webayPort = 5000
    testConfig = {
        "databaseFile" : ":memory:",
        "apis" : {
            "Ebay" : {
                "apiRoot" : f"http://{webayHost}:{webayPort}"
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
        result = asyncio.run(DataManagerUnitTest.dm.getItems())
        self.assertEqual(len(self.dm.itemList), len(result))
        
    def test_addsListingsFromAPIs(self):
        """ When reload is called, the DataManager should go through all the APIs and add their item listings to the database if they aren't there already
        """
        asyncio.run(DataManagerUnitTest.dm.reload())
        result = asyncio.run(DataManagerUnitTest.dm.getListings())
        self.assertEqual(len(asyncio.run(DataManagerUnitTest.dm.getApiListings())), len(result))

    def test_addsNewCustomersFromAPIs(self):
        """ When reload is called, the DataManager should go through all the new orders from the APIs and add any new customers to the database
        """
        asyncio.run(DataManagerUnitTest.dm.reload())
        result = asyncio.run(DataManagerUnitTest.dm.getCustomers())
        customers = set([key['user']['email'] for key in asyncio.run(DataManagerUnitTest.dm.getApiOrders())])
        self.assertEqual(len(customers), len(result))

    def test_addsNewOrdersFromAPIs(self):
        """ When reload is called, the DataManager should go through all the new orders from the APIs and add any new orders to the database
        """
        asyncio.run(DataManagerUnitTest.dm.reload())
        result = asyncio.run(DataManagerUnitTest.dm.getOrders())
        self.assertEqual(len(asyncio.run(DataManagerUnitTest.dm.getApiOrders())), len(result))

    def test_addsLinkBetweenOrderAndListing(self):
        """ When reload is called, the DataManager should go through all the new orders from the APIs and link them to listings
        """
        asyncio.run(DataManagerUnitTest.dm.reload())
        result = asyncio.run(DataManagerUnitTest.dm.getAllOrderListingLinks())
        orders = asyncio.run(DataManagerUnitTest.dm.getApiOrders())
        # one link per item in an order, count the number of links expected
        numLinks = reduce(lambda x, y : x + y, [len(x['items']) for x in orders])
        self.assertEqual(numLinks, len(result))
        
    def test_addCustomerAddsACustomer(self):
        """ The addCustomer method should add a customer
        """
        customersBeforeAddingCustomer = asyncio.run(DataManagerUnitTest.dm.getCustomers())
        asyncio.run(DataManagerUnitTest.dm.addCustomer("John Doe", "johndoe@email.com"))
        customersAfterAddingCustomer = asyncio.run(DataManagerUnitTest.dm.getCustomers())
        self.assertEqual(1, len(customersAfterAddingCustomer) - len(customersBeforeAddingCustomer))

    @classmethod
    def setUpClass(cls):
        # start webay as a separate thread, we can't run these tests without it
        loop = asyncio.new_event_loop()
        DataManagerUnitTest.webayThread = threading.Thread(target=runWebay, args=(DataManagerUnitTest.webayHost, DataManagerUnitTest.webayPort))
        # by setting it to a daemon thread, it will be terminated when the main thread dies
        DataManagerUnitTest.webayThread.setDaemon(True)
        DataManagerUnitTest.webayThread.start()
        return super().setUpClass()

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