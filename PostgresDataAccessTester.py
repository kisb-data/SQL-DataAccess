from Libs import PostgresDataAccess as DA

# Create connection
connection_param = ["postgres", "localhost", "5432", "postgres", "postgres"] 
DataAccess = DA.DataAccess()
DataAccess.SetConnectionData(connection_param)


# Acces to table and column data
table_names = DataAccess. GetTableNames()
column_names = DataAccess. GetColumnNames(table_names)
for table_index in range(len(table_names)):
    print("")
    print("=================")
    print("Table: "+table_names[table_index])
    column_str = "Columns: "
    for column in column_names[table_index]:
        column_str  = column_str + str(column) + " |  "
    print(column_str)

print("")
print("=================")

# create table test
cols = [{"id": "SERIAL PRIMARY KEY"}, {"col1": "VARCHAR(100)"}, {"col2": "VARCHAR(100)"}]
DataAccess.CreateTable("test", cols)

# get column names of test table
table = ["test", ]
print("Columns in the test table: ",DataAccess. GetColumnNames(table))

# insert data in test table
data = [{"col1": "abcd", "col2": "efgh"}, {"col1": "ijkl", "col2": "mnop"}]
print("Returned id: ", DataAccess.Insert("test", data, "id"))

# print test table data
print("Table data: ", DataAccess.SelectAllFromTable("test"))

# delete table
DataAccess.DeleteTable("test")


