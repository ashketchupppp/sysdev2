import unittest
import sqlite3
import os

import context
from src.OnlineStoreDatabase import OnlineStoreDatabase, SQLQuery
    
class OnlineStoreDatabaseUnitTest(unittest.TestCase):
    db = None
    
    def setUp(self):
        """ Create a new database before each test """
        OnlineStoreDatabaseUnitTest.db = OnlineStoreDatabase('test.db')
        
    def tearDown(self):
        """ Delete the database once the test has finished """
        OnlineStoreDatabaseUnitTest.db.connection.close()
        del OnlineStoreDatabaseUnitTest.db
        os.remove('test.db')
    
    def test_generatesTablesOnCreation(self):
        """ The OnlineStoreDatabase should create the tables needed if they don't exist.
            Executing a simple query should be a good enough check to see if the tables are created.
        """
        try:
            customerRows = [x for x in OnlineStoreDatabaseUnitTest.db.executeQuery(SQLQuery.numberRows("customer"))]
            addressRows = [x for x in OnlineStoreDatabaseUnitTest.db.executeQuery(SQLQuery.numberRows("address"))]
            itemRows = [x for x in OnlineStoreDatabaseUnitTest.db.executeQuery(SQLQuery.numberRows("item"))]
            orderRows = [x for x in OnlineStoreDatabaseUnitTest.db.executeQuery(SQLQuery.numberRows("orders"))]
        except OperationalError as e:
            self.fail(f"Encountered '{e}'' whilst checking if database tables existed.")
    
    
class SQLQueryUnitTest(unittest.TestCase):
    def test_sqlCreateTableFromDefinition(self):
        sqlQuery = SQLQuery.createTableFromDefinition("customer", {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "name" : "VARCHAR",
                "email" : "VARCHAR"
            })
        self.assertEqual(sqlQuery, "CREATE TABLE customer (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, email VARCHAR)")
    
if __name__ == "__main__":
    unittest.main()