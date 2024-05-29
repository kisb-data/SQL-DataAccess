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
cols = [{"id": "INTEGER PRIMARY KEY AUTOINCREMENT"}, {"col1": "VARCHAR(100)"}, {"col2": "VARCHAR(100)"}]
data_access.CreateTable("teszt", cols)

# get column names of teszt table
table = [("teszt", )]
print("Columns in the teszt table: ", data_access.GetColumnNames(table))

# insert data in teszt table
data = [{"col1": "abcd"}, {"col2": "efgh"}]
print("Returned id: ", data_access.Insert("teszt", data))

# print teszt table data
print("Table data: ", data_access.SelectAllFromTable("teszt"))

# delete table
data_access.DeleteTable("teszt")