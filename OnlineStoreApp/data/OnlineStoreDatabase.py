import sqlite3
from sqlite3.dbapi2 import IntegrityError
import asyncio

from data.SQLiteDB import SQLiteDB, SQL

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
                "location" : "INTEGER UNIQUE"
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
                f"FOREIGN KEY (itemID, storeID) REFERENCES {listingTable}(itemID, storeID)" : ""
            },
            orderTable : {
                "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                "storesOrderID" : "VARCHAR UNIQUE",
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
        self.db = SQLiteDB(databaseFile)
        
        # setup the database with the tables
        for table in OnlineStoreDatabase.databaseDefinition['tables']:
            self.db.createTable(table, OnlineStoreDatabase.databaseDefinition['tables'][table])
            
            
    # Adding, Updating and Getting Data
    
    ## Updating Data
    
    def setOrderToShipped(self, orderID):
        self.db.update(OnlineStoreDatabase.orderTable, {"status" : "shipped"}, {"id" : orderID})
    
    ## Adding Data
    
    def addCustomer(self, name, email):
        return self.db.add(OnlineStoreDatabase.customerTable, name=name, email=email)
        
    def addItem(self, name, stock, location):
        return self.db.add(OnlineStoreDatabase.itemTable, name=name, stock=stock, location=location)
        
    def addOnlineStore(self, storeName):
        return self.db.add(OnlineStoreDatabase.storeTable, name=storeName)
        
    def addListing(self, itemID, storeID, price):
        return self.db.add(OnlineStoreDatabase.listingTable, itemID=itemID, storeID=storeID, price=price)
    
    def addOrderListingLink(self, orderID, itemID, storeID):
        return self.db.add(OnlineStoreDatabase.orderListingLinkTable, orderID=orderID, itemID=itemID, storeID=storeID)
    
    def addOrder(self, orderDict):
        # make sure we don't have this order already
        order = self.getOrder(orderDict['id'])
        if type(order) == sqlite3.Row:
            return None
        
        # if we don't have this customer yet, add them to the database
        if not self.getCustomer(orderDict['user']['email']):
            self.addCustomer(orderDict['user']['name'], orderDict['user']['email'])
            
        # if we don't have this listing yet, add it to the database
        for item in orderDict['items']:
            self.addListing(item['name'], orderDict['storeID'], item['price'])

        # add the order to the database
        dbOrderDict = {
                "storesOrderID" : orderDict["id"],
                "status": "unprocessed",
                "line1" : orderDict['address']['addressLineOne'],
                "line2" : orderDict['address']['addressLineTwo'],
                "country" : orderDict['address']['country'],
                "streetNameAndNumber" : orderDict['address']["streetNameAndNumber"],
                "postcode" : orderDict['address']['postcode'],
                "customerEmail": orderDict['user']['email'],
        }
        orderRowID = self.db.add(OnlineStoreDatabase.orderTable, dictvalues=dbOrderDict)
        
        # add the order-listing links
        for item in orderDict['items']:
            self.addOrderListingLink(orderRowID, item['name'], orderDict['storeID'])
        
        return orderRowID
        
    ## Getting Data
    
    def getUnprocessedOrders(self):
        return [x for x in self.db.select(OnlineStoreDatabase.orderTable, 
                                          whereDict={"status" : "unprocessed"})]
    
    def getOrderPackingList(self, orderID):
        # get the item listings for the order
        itemListingsForOrder = [x for x in self.db.select(OnlineStoreDatabase.orderListingLinkTable, 
                                                  whereDict={ "orderID" : orderID })]
        # get the actual items from the listings
        itemIDs = [x['itemID'] for x in itemListingsForOrder]
        items = []
        for itemID in itemIDs:
            items += self.db.select(OnlineStoreDatabase.itemTable, whereDict={ "name" : itemID })
        return items
    
    def getAllOrderListingLinks(self):
        return [x for x in self.db.select(OnlineStoreDatabase.orderListingLinkTable)]
    
    def getOrders(self):
        return [x for x in self.db.select(OnlineStoreDatabase.orderTable)]
    
    def getOrder(self, orderID):
        if type(orderID) == str:
            return self.db.getRow(OnlineStoreDatabase.orderTable, storesOrderID=orderID)
        else:
            return self.db.getRow(OnlineStoreDatabase.orderTable, id=int(orderID))
    
    def getItems(self):
        return [x for x in self.db.select(OnlineStoreDatabase.itemTable)]
    
    def getCustomers(self):
        return [x for x in self.db.select(OnlineStoreDatabase.customerTable)]
    
    def getCustomer(self, email):
        return self.db.getRow(OnlineStoreDatabase.customerTable, email=email)
    
    def getOnlineStores(self):
        return [x for x in  self.db.select(OnlineStoreDatabase.storeTable)]
        
    def getListings(self):
        return [x for x in self.db.select(OnlineStoreDatabase.listingTable)]
    
    def getOrdersListings(self, orderID):
        return [x for x in self.db.select(OnlineStoreDatabase.orderListingLinkTable, whereDict={"orderID":orderID})]
    
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
        return self.db.tableHasRow(tableName, whereColumns)
    
    def hasTable(self, tableName):
        try:
            self.cursor.execute(SQL.numberRows(tableName))
            return True
        except sqlite3.OperationalError as e:
            return False