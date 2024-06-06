from Libs.SQLiteDataAccess import DataAccess  # Import the DataAccess class directly
import os

# Create connection
path = os.path.dirname(os.path.abspath(__file__)) + "\\"
db_path = path + "test.sqlite"  # Path to the SQLite database file
data_access = DataAccess(db_path)  # Initialize the DataAccess object

# Access to table and column data
table_names = data_access.GetTableNames()
column_names = data_access.GetColumnNames(table_names)
for table_index in range(len(table_names)):
    print("")
    print("=================")
    print("Table: " + table_names[table_index][0])
    column_str = "Columns: "
    for column in column_names[table_index]:
        column_str = column_str + column[1] + " |  "
    print(column_str)

print("")
print("=================")

# create table test
cols = [{"id": "INTEGER PRIMARY KEY AUTOINCREMENT"}, {"col1": "TEXT"}, {"col2": "TEXT"}]
data_access.CreateTable("test", cols)

# get column names of test table
table = [("test", )]
print("Columns in the test table: ", data_access.GetColumnNames(table))

# insert data in test table
data = [{"col1": "abcd", "col2": "efgh"}, {"col1": "ijkl", "col2": "mnop"}]
print("Returned id: ", data_access.Insert("test", data))

# print test table data
print("Table data: ", data_access.SelectAllFromTable("test"))

# delete table
data_access.DeleteTable("test")

