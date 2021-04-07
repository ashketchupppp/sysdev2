from sqlite3.dbapi2 import IntegrityError, OperationalError
from typing import OrderedDict
import unittest
import sqlite3
import os
import asyncio

from data.OnlineStoreDatabase import OnlineStoreDatabase
from data.SQLiteDB import SQL, SQLiteDB

exampleOrder = {
    "address":{
        "addressLineOne":"Bath and North East Somerset",
        "addressLineTwo":"Icantbearsedtomakeupmoredatatown",
        "country":"United Kingdom",
        "id":"592beaa6-00a4-4c46-b3e3-8d103ebd749a",
        "postcode":"DT2 9HZ",
        "streetNameAndNumber":"19 Madaline Harbors"
    },
    "id":"554de30b-1793-409b-a94c-d24a84582b97",
    "items":[
        {
            "id":"36d05424-1afb-4ed7-ac28-f37ec34e9772",
            "name":"Sony Playstation 4",
            "price":131.01
        },
        {
            "id":"36d05424-1afb-4ed7-ac28-f37ec34e9772",
            "name":"Sony Playstation 4",
            "price":131.01
        }
    ],
    "user":{
        "email":"RoscoePike@hotmail.com",
        "id":"4c8e3056-b6f8-4fe3-b1f7-090930056d38",
        "name":"Roscoe Pike"
    },
    "storeID" : "Ebay"
}

def removeLeftOverDbFiles():
    leftOverDB = [path for path in os.listdir() if ".db" in path]
    for dbFile in leftOverDB:
        try:
            os.remove(dbFile)
        except:
            pass
    
class OnlineStoreDatabaseUnitTest(unittest.TestCase):
    """ Tests the OnlineStoreDatabase class
    """
    db = None
    
    def setUp(self):
        """ Create a new database before each test """
        removeLeftOverDbFiles()
        OnlineStoreDatabaseUnitTest.db = OnlineStoreDatabase(':memory:')
        
    def tearDown(self):
        """ Delete the database once the test has finished """
        del OnlineStoreDatabaseUnitTest.db
        removeLeftOverDbFiles()
    
    def test_addCustomer(self):
        """ The addCustomer method should
             - Add a customer to the customer table and return its ID
             - Return None when unable to add a customer
        """
        OnlineStoreDatabaseUnitTest.db.addCustomer("John Doe", "johndoe@email.com")
        customers = OnlineStoreDatabaseUnitTest.db.getCustomers()
        self.assertTrue(SQLiteDB.rowListContainsRow(customers, {"name":"John Doe", "email": "johndoe@email.com"}))
        
        customerID = OnlineStoreDatabaseUnitTest.db.addCustomer("John Doe", "johndoe@email.com")
        self.assertEqual(None, customerID)

    def test_addItem(self):
        """ The addItem method should
             - Add an item to the items table and return its ID
             - Return None when unable to add an item
        """
        OnlineStoreDatabaseUnitTest.db.addItem("item", 1, 11)
        items = OnlineStoreDatabaseUnitTest.db.getItems()
        self.assertTrue(SQLiteDB.rowListContainsRow(items, {"name" : "item", "stock" : 1, "location" : 11}))
    
        itemID = OnlineStoreDatabaseUnitTest.db.addItem("item", 1, 11)
        self.assertEqual(None, itemID)
        
    def test_addOnlineStore(self):
        """ The addOnlineStore method should
             - Add an online store to the online store table and return its ID
             - Return None when unable to add an online store
        """
        OnlineStoreDatabaseUnitTest.db.addOnlineStore("Ebay")
        stores = OnlineStoreDatabaseUnitTest.db.getOnlineStores()
        self.assertTrue(SQLiteDB.rowListContainsRow(stores, {"name" : "Ebay"}))
        storeID = OnlineStoreDatabaseUnitTest.db.addOnlineStore("Ebay")
        self.assertEqual(None, storeID)
        
    def test_addListing(self):
        """ The addListing method should add a listing to the listing table and return its ID
             - Return None when unable to add a listing
        """
        storeID = OnlineStoreDatabaseUnitTest.db.addOnlineStore("Ebay")
        itemID = OnlineStoreDatabaseUnitTest.db.addItem("door", 1, 11)
        listingID = OnlineStoreDatabaseUnitTest.db.addListing("door", "Ebay", 9.99)
        
        listings = OnlineStoreDatabaseUnitTest.db.getListings()
        self.assertTrue(SQLiteDB.rowListContainsRow(listings, {"itemID" : "door", "storeID" : "Ebay", "price" : 9.99}))
        
        listingID = OnlineStoreDatabaseUnitTest.db.addListing("incorrectKey", "incorrectKey", 9.99)
        self.assertEqual(len(OnlineStoreDatabaseUnitTest.db.getListings()), 1)

    def test_addOrder(self):
        """ The addOrder method should add an order, customer, listing and order-listing link to their tables 
        """
        order = exampleOrder
        # setup the store and items for the order
        OnlineStoreDatabaseUnitTest.db.addOnlineStore(storeName=order['storeID'])
        location = 1
        order = exampleOrder
        for item in order['items']:
            OnlineStoreDatabaseUnitTest.db.addItem(name=item['name'], stock=1, location=location)
            location += 1
        
        orderID = OnlineStoreDatabaseUnitTest.db.addOrder(order)
        
        customers = OnlineStoreDatabaseUnitTest.db.getCustomers()
        listings = OnlineStoreDatabaseUnitTest.db.getListings()
        ordersListingLinks = OnlineStoreDatabaseUnitTest.db.getOrdersListings(orderID)
        orders = OnlineStoreDatabaseUnitTest.db.getOrders()
        
        self.assertTrue(SQLiteDB.rowListContainsRow(customers, {"name" : order['user']['name'], 
                                                                "email" : order['user']['email']}), 
                        msg=customers)
        
        self.assertTrue(SQLiteDB.rowListContainsRow(listings, {"itemID" : order['items'][0]['name'],
                                                               "storeID" : order['storeID'], 
                                                               "price" : order['items'][0]['price']}), 
                        msg=listings)
        
        self.assertTrue(SQLiteDB.rowListContainsRow(orders, {"status": "unprocessed",
                                                             "line1" : order['address']['addressLineOne'],
                                                             "line2" : order['address']['addressLineTwo'],
                                                             "country" : order['address']['country'],
                                                             "streetNameAndNumber" : order['address']['streetNameAndNumber'],
                                                             "postcode" : order['address']['postcode'],
                                                             "customerEmail": order['user']['email']}),
                        msg=orders)
        
        linkID = 1
        for item in order['items']:
            self.assertTrue(SQLiteDB.rowListContainsRow(ordersListingLinks, {"linkID" : linkID,
                                                                            "orderID" : orderID,
                                                                            "itemID" : item['name'],
                                                                            "storeID" : order['storeID']}), 
                            msg=ordersListingLinks)
            linkID += 1
        
        # try to add the order again, make sure it doesn't appear twice
        ordersBeforeDuplicate = OnlineStoreDatabaseUnitTest.db.getOrders()
        orderID = OnlineStoreDatabaseUnitTest.db.addOrder(order)           
        ordersAfterDuplicate = OnlineStoreDatabaseUnitTest.db.getOrders()
        self.assertEqual(len(ordersBeforeDuplicate), len(ordersAfterDuplicate))
            
    def test_getUnprocessedOrders(self):
        """ getUnprocessedOrders should return a list of unprocessed orders
        """
        order = exampleOrder
        # setup the store and items for the order
        OnlineStoreDatabaseUnitTest.db.addOnlineStore(storeName=order['storeID'])
        location = 1
        for item in order['items']:
            OnlineStoreDatabaseUnitTest.db.addItem(name=item['name'], stock=1, location=location)
            location += 1
            
        # add some orders
        orderOne = OnlineStoreDatabaseUnitTest.db.addOrder(order)
        order['id'] = "abcd"
        orderTwo = OnlineStoreDatabaseUnitTest.db.addOrder(order)
        order['id'] = "efgh"
        orderThree = OnlineStoreDatabaseUnitTest.db.addOrder(order)
        
        # mark one of the orders as shipped
        OnlineStoreDatabaseUnitTest.db.setOrderToShipped(orderOne)
        
        # assert that all orders gotten are unprocessed
        unprocessedOrders = OnlineStoreDatabaseUnitTest.db.getUnprocessedOrders()
        for order in unprocessedOrders:
            self.assertTrue(SQLiteDB.rowContainsColumnsWithValues(order, {"status" : 'unprocessed'}), 
                            msg=order)
            
    def test_getOrderPackingList(self):
        """ getOrderPackingList should return a list of items to be packed for an order
        """
        order = exampleOrder
        
        # setup the store and items for the order
        OnlineStoreDatabaseUnitTest.db.addOnlineStore(storeName=order['storeID'])
        location = 1
        for item in order['items']:
            OnlineStoreDatabaseUnitTest.db.addItem(name=item['name'], stock=1, location=location)
            location += 1
            
        # add the order and get the packing list
        orderID = OnlineStoreDatabaseUnitTest.db.addOrder(order)
        packingList = OnlineStoreDatabaseUnitTest.db.getOrderPackingList(orderID)
        
        # assert that the packing list contains the items in the order
        self.assertEqual(2, len(packingList))
        itemNameList = [item['name'] for item in order['items']]
        for itemName in itemNameList:
            self.assertTrue(SQLiteDB.rowListContainsRow(packingList, { "name" : itemName }))

    @classmethod
    def setUpClass(self):
        removeLeftOverDbFiles()

    @classmethod
    def tearDownClass(self):
        removeLeftOverDbFiles()

class SQLUnitTest(unittest.TestCase):
    def test_sqlCreateTableFromDefinition(self):
        sqlQuery = SQL.createTableFromDefinition("customer", {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "name" : "VARCHAR",
                "email" : "VARCHAR"
            })
        self.assertEqual(sqlQuery, "CREATE TABLE customer (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, email VARCHAR)")
    
if __name__ == "__main__":
    unittest.main()