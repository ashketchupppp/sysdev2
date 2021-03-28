import unittest
import sqlite3
import os

import context
from src.OnlineStoreDatabase import OnlineStoreDatabase, SQL

def removeLeftOverDbFiles():
    leftOverDB = [path for path in os.listdir() if ".db" in path]
    for dbFile in leftOverDB:
        try:
            os.remove(dbFile)
        except:
            pass
    
class OnlineStoreDatabaseUnitTest(unittest.TestCase):
    db = None
    
    def setUp(self):
        """ Create a new database before each test """
        removeLeftOverDbFiles()
        OnlineStoreDatabaseUnitTest.db = OnlineStoreDatabase('test.db')
        
    def tearDown(self):
        """ Delete the database once the test has finished """
        OnlineStoreDatabaseUnitTest.db.connection.close()
        del OnlineStoreDatabaseUnitTest.db
        removeLeftOverDbFiles()
    
    def test_generatesTablesOnCreation(self):
        """ The OnlineStoreDatabase should create the tables needed if they don't exist.
            Executing a simple query should be a good enough check to see if the tables are created.
        """
        try:
            for table in OnlineStoreDatabase.databaseDefinition['tables']:
                result = [x for x in OnlineStoreDatabaseUnitTest.db.executeQuery(SQL.numberRows(table))]
        except OperationalError as e:
            self.fail(f"Encountered '{e}'' whilst checking if database tables existed.")

    @classmethod
    def setUpClass(self):
        removeLeftOverDbFiles()

    @classmethod
    def tearDownClass(self):
        removeLeftOverDbFiles()

#    def test_addListing(self):
#        """ Should be able to add a listing for an online store using the addListing method 
#        """
#        OnlineStoreDatabaseUnitTest.db.addStore("Ebay")
#        OnlineStoreDatabaseUnitTest.db.addListing("Item name", 1.23, "Ebay")
#        listings = OnlineStoreDatabaseUnitTest.db.getListings()
#        self.assertEqual(1, len(listings))

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