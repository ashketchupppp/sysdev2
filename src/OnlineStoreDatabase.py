import sqlite3

class SQL:
    """ Utility class to help with constructing SQL queries
    """
    @classmethod
    def createTableFromDefinition(self, tableName, tableDefinition):
        columnStr = ", ".join([f"{column} {tableDefinition[column]}" for column in tableDefinition])
        return f"CREATE TABLE {tableName} ({columnStr})"

    @classmethod
    def select(self, columnsToSelect, table, joins=None, where=None):
        columnStr = ", ".join(columnsToSelect)
        whereStr = ""
        joinStr = ""
        if where != None:
            whereStr = f'WHERE ({where})'
        if joins != None:
            joinStr = " ".join(joins)
        return f'SELECT {columnsToSelect} FROM {table} {joinStr} {whereStr}'
    
    @classmethod
    def numberRows(self, tableName):
        return f"SELECT count(*) FROM {tableName};"
    
    @classmethod
    def tableColumns(self, tableName):
        return f"PRAGMA table_info({tableName})"
    
    @classmethod
    def insertInto(self, tableName, columnsValueDict):
        columnString = ", ".join(columnsValueDict)
        # wrap all the strings in quotes
        for col in columnsValueDict:
            if type(columnsValueDict[col]) == str:
                columnsValueDict[col] = f'"{columnsValueDict[col]}"'
        valueString = ", ".join([str(columnsValueDict[key]) for key in columnsValueDict])
        return f'INSERT INTO {tableName} ({columnString}) VALUES ({valueString});'

class OnlineStoreDatabase:
    storeTable = 'onlineStore'
    listingTable = 'listing'
    orderTable = 'orders'
    customerTable = 'customer'
    itemTable = 'items'
    orderListingLinkTable = "orderListingLink"
    
    databaseDefinition = {
        "tables" : {
            storeTable : {
                "name" : "VARCHAR PRIMARY KEY"
            },
            customerTable : {
                "name" : "VARCHAR",
                "email" : "VARCHAR PRIMARY KEY"
            },
            itemTable : {
                "name" : "VARCHAR PRIMARY KEY",
                "stock" : "INTEGER",
                "location" : "INTEGER"
            },
            listingTable : {
                "itemID" : "VARCHAR",
                "storeID" : f"VARCHAR",
                "price" : "DOUBLE",
                f"FOREIGN KEY (storeID) REFERENCES {storeTable}(name)" : "",
                f"FOREIGN KEY (itemID) REFERENCES {itemTable}(name)" : "",
                "PRIMARY KEY (itemID, storeID)" : ""
            },
            orderListingLinkTable : {
                "linkID" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "orderID" : "INTEGER",
                "itemID" : "VARCHAR",
                "storeID" : "VARCHAR",
                f"FOREIGN KEY (orderID) REFERENCES {orderTable}(id)" : "",
                f"FOREIGN KEY (itemID) REFERENCES {listingTable}(itemID)" : "",
                f"FOREIGN KEY (storeID) REFERENCES {listingTable}(storeID)" : "",
            },
            orderTable : {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "status": "VARCHAR",
                "line1" : "VARCHAR",
                "line2" : "VARCHAR",
                "country" : "VARCHAR",
                "streetNameAndNumber" : "VARCHAR",
                "postcode" : "VARCHAR",
                "customerEmail": f"VARCHAR",
                f"FOREIGN KEY (customerEmail) REFERENCES {customerTable}(email)" : ""
            }
        }
    }
    
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        self.connection = None
        self.cursor = None
        self.connect(databaseFile)
        
        # setup the database with the tables
        for table in OnlineStoreDatabase.databaseDefinition['tables']:
            if not self.hasTable(table):
                query = SQL.createTableFromDefinition(table, OnlineStoreDatabase.databaseDefinition['tables'][table])
                self.executeQuery(query)
                
    def insert(self, table, values : dict):
        self.executeQuery(SQL.insertInto(table, values))
        return self.cursor.lastrowid
        
    def select(self, table, columns="*", whereStr=None, joins=None):
        return [x for x in self.executeQuery(SQL.select(columns, table, where=whereStr, joins=joins))]
                
    def addListing(self, itemID, storeID):
        values = {
            "storeID" : storeID,
            "itemID" : itemID
        }
        self.executeQuery(SQL.insertInto(OnlineStoreDatabase.listingTable, values))
        
    def getListings(self):
        result = self.executeQuery(SQL.select("*", OnlineStoreDatabase.listingTable))
        return [x for x in result]
    
    def hasItem(self, name):
        whereStr = f'name="{name}"'
        return bool([x for x in self.executeQuery(SQL.select("*", OnlineStoreDatabase.itemTable, whereStr=whereStr))])
        
    def hasListing(self, itemID : int, storeID : int):
        whereStr = f'storeID={storeID}, itemID={itemID}'
        return bool([x for x in self.executeQuery(SQL.select("*", OnlineStoreDatabase.listingTable, whereStr=whereStr))])
    
    def has(self, table, whereValues={}, joinList=None):
        for val in whereValues:
            if type(whereValues[val]) == str:
                whereValues[val] = f'"{whereValues[val]}"'
        whereStr = ", ".join([f'{key}={whereValues[key]}' for key in whereValues])
        return bool(self.select(table, whereStr=whereStr, joins=joinList))
    
    def close(self):
        self.connection.close()
    
    def connect(self, filepath):
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
    
    def isConnected(self):
        return True if self.connection != None else False

    def tableHasColumns(self, table, columns):
        tableColumns = self.cursor.execute(SQL.tableColumns(table))
        for col in tableColumns:
            if not col[1] in columns:
                return False
        return True
    
    def tableHasRow(self, tableName, whereColumns):
        result = [x for x in self.executeQuery(SQL.select("*", tableName, where=whereColumns))]
        return True if len(result) > 0 else False
    
    def hasTable(self, tableName):
        try:
            self.cursor.execute(SQL.numberRows(tableName))
            return True
        except sqlite3.OperationalError as e:
            return False
    
    def executeQuery(self, queryStr):
        result = self.cursor.execute(queryStr)
        self.connection.commit()
        return result