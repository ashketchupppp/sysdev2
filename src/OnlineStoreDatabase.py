import sqlite3

class SQL:
    """ Utility class to help with constructing SQL queries
    """
    @classmethod
    def createTableFromDefinition(self, tableName, tableDefinition):
        columnStr = ", ".join([f"{column} {tableDefinition[column]}" for column in tableDefinition])
        return f"CREATE TABLE {tableName} ({columnStr})"
    
    @classmethod
    def select(self, columnsToSelect, table, whereStr=None):
        columnStr = ", ".join(columnsToSelect)
        if whereStr != None:
            return f'SELECT {columnStr} FROM {table} WHERE {whereStr}'
        else:
            return f'SELECT {columnStr} FROM {table}'
    
    @classmethod
    def numberRows(self, tableName):
        return f"SELECT count(*) FROM {tableName};"
    
    @classmethod
    def tableColumns(self, tableName):
        return f"PRAGMA table_info({tableName})"
    
    @classmethod
    def insertInto(self, tableName, columnsValueDict):
        columnString = ", ".join(columnsValueDict)
        valueString = ", ".join([str(columnsValueDict[key]) for key in columnsValueDict])
        return f'INSERT INTO {tableName} ({columnString}) VALUES ({valueString});'

class OnlineStoreDatabase:
    storeTable = 'onlineStore'
    listingTable = 'listing'
    orderTable = 'orders'
    customerTable = 'customer'
    itemTable = 'items'
    
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
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "name" : "VARCHAR",
                "price" : "DOUBLE",
                "stock" : "INTEGER",
                "location" : "INTEGER"
            },
            listingTable : {
                "itemID" : "INTEGER",
                "storeID" : f"VARCHAR",
                f"FOREIGN KEY (storeID) REFERENCES {storeTable}(name)" : "",
                f"FOREIGN KEY (itemID) REFERENCES {itemTable}(id)" : "",
                "PRIMARY KEY (itemID, storeID)" : ""
            },
            "orderItemLink" : {
                "orderID" : f"INTEGER",
                "listingID" : f"INTEGER",
                "PRIMARY KEY (orderID, listingID)" : "",
                f"FOREIGN KEY (orderID) REFERENCES {orderTable}(id)" : "",
                f"FOREIGN KEY (listingID) REFERENCES {listingTable}(id)" : ""
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
    
    presetItems = [
        {'name': 'Sony Playstation 4', 'price': 131.01, 'location' : 1}, 
        {'name': 'Headphones', 'price': 119.08, 'location' : 2}, 
        {'name': 'Wireless Mouse', 'price': 134.12, 'location' : 3}, 
        {'name': 'Nintendo Switch', 'price': 6.4, 'location' : 4}, 
        {'name': 'iPhone 7 Plus', 'price': 64.4, 'location' : 5}, 
        {'name': 'Galaxy S9 Edge', 'price': 47.76, 'location' : 6}, 
        {'name': 'Laptop', 'price': 210.37, 'location' : 7}, 
        {'name': 'Chair', 'price': 378.46, 'location' : 8}, 
        {'name': 'Trumpet', 'price': 282.24, 'location' : 9}, 
        {'name': 'Plate', 'price': 8.73, 'location' : 10}, 
        {'name': 'Mug', 'price': 402.51, 'location' : 11}, 
        {'name': 'Door', 'price': 283.64, 'location' : 12}, 
        {'name': 'Original Van Gogh', 'price': 33.92, 'location' : 13}, 
        {'name': 'Candle', 'price': 99.06, 'location' : 14}
    ]
    
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        self.connection = None
        self.cursor = None
        self.connect(databaseFile)
        
        # setup the database with the tables
        for table in OnlineStoreDatabase.databaseDefinition['tables']:
            if not self.hasTable(table) or not self.tableHasColumns(table, [column for column in table]):
                query = SQL.createTableFromDefinition(table, OnlineStoreDatabase.databaseDefinition['tables'][table])
                self.executeQuery(query)
                
    def addOrder(self, orderDict):
        # if we don't have the customers email, add them to the database
        pass
    
    def addStore(self, name):
        self.executeQuery(SQL.insertInto(OnlineStoreDatabase.storeTable, {'name' : f'"{name}"'}))
                
    def addListing(self, name, price, storeID, stock=0):
        values = {
            "name" : f'"{name}"',
            "stock" : stock,
            "price" : price,
            "storeID" : f'"{storeID}"'
        }
        self.executeQuery(SQL.insertInto(OnlineStoreDatabase.listingTable, values))
        
    def getListings(self):
        result = self.executeQuery(SQL.select("*", OnlineStoreDatabase.listingTable))
        return [x for x in result]
        
    def hasListing(self, name, price, store):
        whereStr = f'name="{name}"' # , price={price}, storeID="{store}"
        return bool([x for x in self.executeQuery(SQL.select("*", OnlineStoreDatabase.listingTable, whereStr=whereStr))])
        
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
        result = [x for x in self.executeQuery(SQL.select("*", tableName, whereColumns))]
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