import sqlite3
import os

class DataAccess:
    # constructor
    def __init__(self, db_path, debug=False):
        self.db_path = db_path
        self.last_error = ""

    def ResetLastError(self):
        self.last_error=""
    
    def GetLastError(self):
        return(self.last_error)

    # create connection
    def Connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            self.last_error=str(e)
            return None

    # write/create
    def SQLiteWrite(self, command: str, ret=False):
        id = None
        conn = self.Connection()
        if conn is None:
            return

        try:
            with conn:
                cur = conn.cursor()
                cur.execute(command)
                if ret:
                    id = cur.lastrowid
        except sqlite3.Error as e:
            self.last_error=str(e)
        finally:
            if conn:
                conn.close()
        return id

    # read data
    def SQLiteRead(self, command: str):
        conn = self.Connection()
        if conn is None:
            return None
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(command)
                ret = cur.fetchall()
            return ret
        except sqlite3.Error as e:
            self.last_error=str(e)
            return None
        finally:
            if conn:
                conn.close()

    # get table names
    def GetTableNames(self):
        command = "SELECT name FROM sqlite_master WHERE type='table';"
        self.logger.debug(command)
        return self.SQLiteRead(command)

    # get column names of table
    def GetColumnNames(self, tables: list):
        ret = list()
        for table in tables:
            command = f"PRAGMA table_info({table[0]});"
            column_info = self.SQLiteRead(command)
            columns = [col[1] for col in column_info] 
            ret.append(columns)
        return ret

    # create table
    def CreateTable(self, table_name: str, columns: list, additional_str=""):
        self.DeleteTable(table_name)

        cols = ""
        for column in columns:
            keys = list(column.keys())
            values = list(column.values())
            cols += f"{keys[0]} {values[0]}, "

        cols = cols.rstrip(', ')

        command = f"CREATE TABLE {table_name} ({cols}"

        if additional_str != "":
            command += ", " + additional_str
        command += ");"

        self.SQLiteWrite(command)

    # insert data in table
    def Insert(self, table=str, data=list(), return_value=""):
        col = ""
        val = ""

        for i in range(len(data)):
            keys = list(data[i].keys())
            values = list(data[i].values())

            col += f"{keys[0]}"
            val += f"'{values[0]}'"

            if i < len(data) - 1:
                col += ", "
                val += ", "

        command = f"INSERT INTO {table} ({col}) VALUES ({val})"
        
        if return_value != "":
            command += " RETURNING " + return_value
        command += ";"

        return self.SQLiteWrite(command, ret=True)

    # get table data
    def SelectAllFromTable(self, table):
        command = "SELECT * FROM " + table + ";"
        return self.SQLiteRead(command)

    # get custom data
    def SelectCustom(self, command: str):
        return self.SQLiteRead(command)

    # delete table
    def DeleteTable(self, table_name):
        command = "DROP TABLE IF EXISTS " + table_name + ";"
        self.SQLiteWrite(command)

    # create database 
    def CreateDatabase(self, path):
        os.remove(path)