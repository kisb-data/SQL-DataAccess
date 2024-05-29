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
    print("Table: "+table_names[table_index][0])
    column_str = "Columns: "
    for column in column_names[table_index]:
        column_str  = column_str + column[0] + " |  "
    print(column_str)

print("")
print("=================")

# create table test
cols = [{"id": "SERIAL PRIMARY KEY"}, {"col1": "VARCHAR(100)"}, {"col2": "VARCHAR(100)"}]
DataAccess.CreateTable("teszt", cols)

# get column names of teszt table
table = [("teszt", )]
print("Columns in the teszt table: ",DataAccess. GetColumnNames(table))

# insert data in teszt table
data = [{"col1": "abcd"}, {"col2": "efgh"}]
print("Returned id: ", DataAccess.Insert("teszt", data, "id"))

# print teszt table data
print("Table data: ", DataAccess.SelectAllFromTable("teszt"))

# delete table
DataAccess.DeleteTable("teszt")


