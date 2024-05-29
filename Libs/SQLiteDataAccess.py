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
        return self.SQLiteRead(command)

    # get column names of table
    def GetColumnNames(self, tables: list):
        ret = list()
        for table in tables:
            command = f"PRAGMA table_info({table[0]});"
            column_info = self.SQLiteRead(command)
            columns = [col[1] for col in column_info]  # Extract only column names
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

        self.logger.debug(command)

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

    # create database (not applicable in SQLite, databases are files)
    def CreateDatabase(self, database_name):
        self.logger.warning("CreateDatabase method is not applicable in SQLite. Databases are managed as files.")