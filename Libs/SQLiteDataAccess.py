import sqlite3
import logging
import os

class DataAccess:
    # constructor
    def __init__(self, db_path, debug=False):
        self.db_path = db_path

        # print info
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('----------> %(asctime)s - %(levelname)s - %(funcName)s:  %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # if debug, write to log file
        if debug:
            file_handler = logging.FileHandler(str(os.path.dirname(os.path.abspath(__file__)) + "/log.txt"))
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    # create connection
    def Connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            self.logger.warning("Error while connecting. " + str(e))
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
            self.logger.warning("Error by writing/creating. " + str(e))
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
            self.logger.warning("Error by reading data. " + str(e))
            return None
        finally:
            if conn:
                conn.close()

    # get table names
    def GetTableNames(self):
        command = "SELECT name FROM sqlite_master WHERE type='table';"
        self.logger.debug(command)
        ret = self.SQLiteRead(command)
        tables= [item[0] for item in ret]
        return tables

    # get column names of table
    def GetColumnNames(self, tables: list):
        ret = list()
        for table in tables:
            command = f"PRAGMA table_info({table});"
            column_info = self.SQLiteRead(command)
            columns = [col[1] for col in column_info] 
            ret.append(columns)
        return ret

    # create table
    def CreateTable(self, table_name: str, columns: list, additional_str=""):

        cols = ""
        for column in columns:
            keys = list(column.keys())
            values = list(column.values())
            cols += f"{keys[0]} {values[0]}, "

        cols = cols.rstrip(', ')

        command = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols}"

        if additional_str != "":
            command += ", " + additional_str
        command += ");"

        self.logger.debug(command)
      
        self.SQLiteWrite(command)

    # insert data in table
    def Insert(self, table=str, data=list(), return_value=""):
        columns = ""
        values_list = []

        if not data:
            raise ValueError("Data cannot be empty")

        # Extract column names from the first dictionary (assuming all dictionaries have the same keys)
        columns = ", ".join(data[0].keys())

        # Construct values part for each row
        for row in data:
            values = ", ".join(f"'{value}'" for value in row.values())
            values_list.append(f"({values})")

        # Join all rows for the VALUES part
        values = ", ".join(values_list)
        
        command = f"INSERT INTO {table} ({columns}) VALUES {values}"

        if return_value:
            command += " RETURNING " + return_value
        command += ";"

        self.logger.debug(command)

        return self.SQLiteWrite(command, ret=True)

    # get table data
    def SelectAllFromTable(self, table):
        command = "SELECT * FROM " + table + ";"
        self.logger.debug(command)
        return self.SQLiteRead(command)

    # get custom data
    def SelectCustom(self, command: str):
        self.logger.debug(command)
        return self.SQLiteRead(command)

    # delete table
    def DeleteTable(self, table_name):
        command = "DROP TABLE IF EXISTS " + table_name + ";"
        self.logger.debug(command)
        self.SQLiteWrite(command)

    # delete database 
    def DeleteDatabase(self, path):
        os.remove(path)
        self.logger.debug("Database deleted. ("+path+")")