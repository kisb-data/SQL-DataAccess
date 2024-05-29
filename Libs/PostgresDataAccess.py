import psycopg2
import logging
import os

# DataAccess class
class DataAccess:

       # constructor
    def __init__(self, debug = False):
        self.dbname = "",
        self.host = "",
        self.port = "",
        self.user = "",
        self.password = ""

        # print info
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('---------->' '%(asctime)s - %(levelname)s - %(funcName)s:  %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # if debug, write to log file
        if debug: 
            file_handler = logging.FileHandler(str(os.path.dirname(os.path.abspath(__file__))+"\\log.txt"))
            file_handler.setLevel(logging.DEBUG)  
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)


    # set connection parameters
    def SetConnectionData(self, conn_set: list):
        
        # check if the list of connection data is ok
        if len(conn_set) != 5:
                self.logger.error("Connection data need to be size of 5. , Your list is the size of: " +str(len(conn_set)))

        self.dbname = conn_set[0]
        self.host = conn_set[1]
        self.port = conn_set[2]
        self.user = conn_set[3]
        self.password = conn_set[4]
        self.logger.info("Connection parameters: ")
        self.logger.info(f"DatabaseName: '{conn_set[0]}', Host: '{conn_set[1]}', Port: '{conn_set[2]}', User: '{conn_set[3]}', Password: '{conn_set[4]}',")
        

    # create connection
    def Connection(self):
        try:
            conn = psycopg2.connect(
            dbname = self.dbname,
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password)

        except psycopg2.Error as e:
            self.logger.warning("Error while connecting. "+str(e))
            return None
        
        return conn
    

    # write/create
    def PostgresWrite(self, command: str, ret = False):
        id = None
        conn = self.Connection()
        if conn == None:
            return 
        
        try:
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            if ret:
                id = cur.fetchone()[0]
            conn.close()

        except psycopg2.Error as e:
            conn.rollback()
            self.logger.warning("Error by writing/creating. "+str(e))

        return id


    # read data
    def PostgresRead(self, command: str):

        conn = self.Connection()
        if conn == None:
            return None
        try:
            cur = conn.cursor()
            cur.execute(command)
            ret= cur.fetchall()
            conn.close()

        except psycopg2.Error as e:
            conn.rollback()
            self.logger.warning("Error by reading data. "+str(e))

        return ret


    # get table names
    def GetTableNames(self):
        command ="SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
        self.logger.debug(command)
        return self.PostgresRead(command)


    # get column names of table
    def GetColumnNames(self, tables: list):

        ret = list()
 
        for table in tables:
            command = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}';"
            ret.append(self.PostgresRead(command))
        return ret
    

    # create table
    def CreateTable(self, table_name: str, columns: list, additional_str = ""):
       
        self.DeleteTable(table_name)

        cols = ""
        for column in columns:
            keys = list(column.keys())
            values = list(column.values())
            cols += f"{keys[0]} {values[0]}, "
    
        cols = cols.rstrip(', ')

        command = f"CREATE TABLE {table_name} ({cols}"

        if additional_str!= "":
            command += ", " + additional_str 
        command += ");"

        self.logger.debug(command)

        self.PostgresWrite(command)


    # insert data in table
    def Insert(self, table = str, data = list(), return_value = ""):
        
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
            command += "RETURNING " + return_value 
        command += ";"
      
        self.logger.debug(command)
        
        return self.PostgresWrite(command, ret=True)

      
    # get table data
    def SelectAllFromTable(self, table):
        command = "SELECT * FROM " + table + ";"
        self.logger.debug(command)
        return(self.PostgresRead(command))

    # get custom data
    def SelectCustom(self, command: str):
        self.logger.debug(command)
        return(self.PostgresRead(command))
    
    # ddelete
    def DeleteTable(self, table_name):
        command = "DROP TABLE IF EXISTS "+table_name+";"
        self.logger.debug(command)
        self.PostgresWrite(command)

    # create database
    def CreateDatabase(self, database_name):
        command = "CREATE DATABASE "+database_name+";"
        self.logger.debug(command)
        self.PostgresWrite(command)