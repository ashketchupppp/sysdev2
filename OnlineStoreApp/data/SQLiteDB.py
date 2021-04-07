import sqlite3
from sqlite3.dbapi2 import IntegrityError, OperationalError

class SQL:
    """ Utility class to help with constructing SQL queries
    """
    
    @classmethod
    def dictToSQLKeyValueList(self, Dict):
        List = []
        for key in Dict:
            if type(Dict[key]) == str:
                List.append(f'{key}="{Dict[key]}"')
            else:
                List.append(f"{key}={Dict[key]}")
        return ", ".join(List)
    
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
            whereStrs = []
            for key in where:
                if type(where[key]) == str:
                    whereStrs.append(f'{key}="{where[key]}"')
                else:
                    whereStrs.append(f"{key}={where[key]}")
            whereStr = f'WHERE ({", ".join(whereStrs)})'
        if joins != None:
            joinStr = " ".join(joins)
        return f'SELECT {columnStr} FROM {table} {joinStr} {whereStr}'
    
    @classmethod
    def numberRows(self, tableName):
        return f"SELECT count(*) FROM {tableName};"
    
    @classmethod
    def tableColumns(self, tableName):
        return f"PRAGMA table_info({tableName})"
    
    @classmethod
    def update(self, table, columnsToUpdateDict, whereDict):
        columnStr = SQL.dictToSQLKeyValueList(columnsToUpdateDict)
        whereStr = SQL.dictToSQLKeyValueList(whereDict)
        return f'UPDATE {table} SET {columnStr} WHERE {whereStr};'
    
    @classmethod
    def insertInto(self, tableName, columnsValueDict):
        columnString = ", ".join(columnsValueDict)
        # wrap all the strings in quotes
        for col in columnsValueDict:
            if type(columnsValueDict[col]) == str:
                columnsValueDict[col] = f'"{columnsValueDict[col]}"'
        valueString = ", ".join([str(columnsValueDict[key]) for key in columnsValueDict])
        return f'INSERT INTO {tableName} ({columnString}) VALUES ({valueString});'


class SQLiteDB:
    """ Manages a connection to an sqlite3 database and provides functions for interacting with the database.
        This is for interacting with an sqlite3 database in a generic manner rather than one that is specific to this application
    """
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        self.connection = None
        self.cursor = None
        self.connect(databaseFile)
        
    def close(self):
        self.connection.close()
    
    def connect(self, filepath):
        self.connection = sqlite3.connect(filepath)
        
        # set the connection to return sqlite3.Row objects instead of tuples
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
        # sqlite3 doesn't maintain referential integrity by default, turn it on
        self.executeQuery("PRAGMA foreign_keys = 1")
    
    def isConnected(self):
        return True if self.connection != None else False
    
    # Utility Class methods for general ease of handling sqlite3.Row objects
        
    @classmethod
    def rowContainsColumnsWithValues(self, row : sqlite3.Row, keyValueDict, ignoreExtras=True):
        """ Returns True if the passed row object contains all the keys and values in the keyValueDict
            Note that you can check for a single key value pair, or you can check for all of them. 
            Any extra keys in the row object will be ignored.
        """
        containsAll = True
        for key in keyValueDict:
            try:
                if row[key] != keyValueDict[key]:
                    containsAll = False
            except IndexError:
                raise IndexError(f"No item with the key {key}")
        return containsAll
    
    @classmethod
    def rowListContainsRow(self, rowList, keyValueDict):
        """ Calls rowContainsColumnsWithValues on each sqlite3.Row object in the rowList, 
        returns True if it finds a row that contains all the key/value pairs passed
        """
        for row in rowList:
            if self.rowContainsColumnsWithValues(row, keyValueDict):
                return True
        return False
    
    # Mid-Level Database Functions
    
    def getRow(self, table, columns=["*"], whereValues=None, **wherekwvalues):
        """ Retrieves a row from a table.
            Columns should be a list of columns (str)
            whereValues should be a dictionary of key/value pairs to use in the where statement
            the whereValues can also be passed as keyword arguments, leaving whereValues as None
        """
        if whereValues == None:
            whereValues = dict(wherekwvalues)
        # return self.select(table, columns, whereValues)
        result = self.select(table, columns, whereValues)
        if len(result) == 1:
            return result[0]
        else:
            return None
    
    def add(self, table, dictvalues=None, **kwvalues):
        """ Inserts a row into the passed table with the passed dictvalues.
        """
        if dictvalues == None:
            values = dict(kwvalues)
        else:
            values = dictvalues
        try:
            return self.insert(table, values)
        except IntegrityError:
            return None
        
    def createTable(self, tableName, tableDefinition):
        try:
            query = SQL.createTableFromDefinition(tableName, tableDefinition)
            self.executeQuery(query)
            return True
        except OperationalError:
            return None
        
    def hasTable(self, tableName):
        try:
            self.cursor.execute(SQL.numberRows(tableName))
            return True
        except sqlite3.OperationalError as e:
            return False
        
    def tableHasRow(self, tableName, whereColumns):
        result = [x for x in self.executeQuery(SQL.select("*", tableName, where=whereColumns))]
        return True if len(result) > 0 else False
    
    # Low-Level SQL Functions
                
    def insert(self, table, values : dict):
        self.executeQuery(SQL.insertInto(table, values))
        return self.cursor.lastrowid

    def select(self, table, columns=['*'], whereDict=None, joins=None):
        self.executeQuery(SQL.select(columns, table, where=whereDict, joins=joins))
        return self.cursor.fetchall()
    
    def update(self, table, columnsToChangeDict, whereDict):
        self.executeQuery(SQL.update(table, columnsToChangeDict, whereDict))
    
    def executeQuery(self, queryStr):
        result = self.cursor.execute(queryStr)
        self.connection.commit()
        return result