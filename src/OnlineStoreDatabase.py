import sqlite3

class SQLQuery:
    @classmethod
    def createTableFromDefinition(self, tableName, tableDefinition):
        columnStr = ", ".join([f"{column} {tableDefinition[column]}" for column in tableDefinition])
        return f"CREATE TABLE {tableName} ({columnStr})"
    
    @classmethod
    def numberRows(self, tableName):
        return f"SELECT count(*) FROM {tableName};"
    
    @classmethod
    def tableColumns(self, tableName):
        return f"PRAGMA table_info({tableName})"

class OnlineStoreDatabase:
    databaseDefinition = {
        "tables" : {
            "customer" : {
                "name" : "VARCHAR",
                "email" : "VARCHAR PRIMARY KEY"
            },
            "address" : {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "line1" : "VARCHAR",
                "line2" : "VARCHAR",
                "country" : "VARCHAR",
                "streetNameAndNumber" : "VARCHAR",
                "postcode" : "VARCHAR"
            },
            "item" : {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "name" : "VARCHAR",
                "stock" : "INTEGER",
                "price" : "DOUBLE"
            },
            "orders" : {
                "status": "VARCHAR",
                "customerID": "INTEGER",
                "addressID": "INTEGER",
                "itemID": "INTEGER",
                "PRIMARY KEY (customerID, addressID, itemID)" : ""
            }
        }
    }
    
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        self.connection = None
        self.cursor = None
        self.connect(databaseFile)
        
        for table in OnlineStoreDatabase.databaseDefinition['tables']:
            if not self.hasTable(table) or not self.tableHasColumns(table, [column for column in table]):
                query = SQLQuery.createTableFromDefinition(table, OnlineStoreDatabase.databaseDefinition['tables'][table])
                self.executeQuery(query)
                
    def close(self):
        self.connection.close()
    
    def connect(self, filepath):
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
    
    def isConnected(self):
        return True if self.connection != None else False
    
    def tableHasColumns(self, table, columns):
        tableColumns = self.cursor.execute(SQLQuery.tableColumns(table))
        for col in tableColumns:
            if not col[1] in columns:
                return False
        return True
    
    def hasTable(self, tableName):
        try:
            self.cursor.execute(SQLQuery.numberRows(tableName))
            return True
        except sqlite3.OperationalError as e:
            return False
    
    def executeQuery(self, queryStr):
        return self.cursor.execute(queryStr)
