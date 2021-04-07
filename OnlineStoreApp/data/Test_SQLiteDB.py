import unittest
import os
import sqlite3
import asyncio

from data.SQLiteDB import SQL, SQLiteDB
from data.OnlineStoreDatabase import OnlineStoreDatabase

class SQLiteDB_UnitTests(unittest.TestCase):
    """ Tests the SQLiteDB class.
    """
    db = None
    
    def setUp(self):
        # create the testing database
        SQLiteDB_UnitTests.db = SQLiteDB(":memory:")
        for table in OnlineStoreDatabase.databaseDefinition['tables']:  
            SQLiteDB_UnitTests.db.createTable(table, OnlineStoreDatabase.databaseDefinition['tables'][table])
            
        # put some fake data in there
        SQLiteDB_UnitTests.db.insert(OnlineStoreDatabase.customerTable, {"name":"John", "email":"johnsemail@email.com"})
        SQLiteDB_UnitTests.db.insert(OnlineStoreDatabase.customerTable, {"name":"Jack", "email":"jacksemail@email.com"})
        SQLiteDB_UnitTests.db.insert(OnlineStoreDatabase.customerTable, {"name":"Jill", "email":"jillsemail@email.com"})
        
    def tearDown(self):
        SQLiteDB_UnitTests.db.close()
        del SQLiteDB_UnitTests.db
        return super().tearDown()

    def test_select(self):
        result = SQLiteDB_UnitTests.db.select(OnlineStoreDatabase.customerTable, ["*"])
        self.assertTrue(SQLiteDB.rowListContainsRow(result, {"name":"John", "email": "johnsemail@email.com"}))
        
    def test_getRow(self):
        # test getting a simple row
        result = SQLiteDB_UnitTests.db.getRow(OnlineStoreDatabase.customerTable, ["*"], email="johnsemail@email.com")
        self.assertTrue(SQLiteDB.rowContainsColumnsWithValues(result, {"name":"John", "email": "johnsemail@email.com"}))
        
    def test_update(self):
        SQLiteDB_UnitTests.db.update(OnlineStoreDatabase.customerTable, {"name" : "John Smith"}, {"email" : "johnsemail@email.com"})
        result = SQLiteDB_UnitTests.db.getRow(OnlineStoreDatabase.customerTable, ["*"], email="johnsemail@email.com")
        self.assertTrue(SQLiteDB.rowContainsColumnsWithValues(result, {"name":"John Smith", "email": "johnsemail@email.com"}))
        
        
        
if __name__ == "__main__":
    unittest.main()