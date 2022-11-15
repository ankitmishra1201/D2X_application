import sqlite3
import pandas as pd



def readExcel(fileName):
    try:
        df = pd.read_excel(fileName)
    except:
        return None
    return df

class Database:
    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.df = readExcel(self.fileName)
            if(self.df is None):
                raise Exception
        except:
            print("File name entered doesn't exist, please enter valid name.")
            return
        try:
            self.conn = sqlite3.connect("Database.db")
        except:
            print("Connection to database unsuccessfull.")
        self.tableName = "student"
        self.columnNames = [columnName for columnName in self.df]
        return
    def generateCreateTableQuery(self):
        self.createTableQuery = "Create table "
        self.createTableQuery += (self.tableName + "(")
        count = 0
        for column in self.df:
            if(count==0):
                self.createTableQuery += (column+" text primary key not null unique, ")
            elif(count==(len(self.columnNames)-1)):
                self.createTableQuery += (column+" text)")
            else:
                self.createTableQuery += (column+" text, ")
            count += 1
        return self.createTableQuery
    def generateInsertTableQuery(self):
        self.insertTableQuery = "insert into "
        self.insertTableQuery += (self.tableName + "(")
        count = 0
        questionString = ""
        for column in self.columnNames:
            if(count==(len(self.columnNames)-1)):
                self.insertTableQuery += (column + ") values(")
                questionString += ("?)")
            else:
                self.insertTableQuery += (column + ", ")
                questionString += "?, "
            count += 1
        self.insertTableQuery += questionString
        return self.insertTableQuery
    def createDatabase(self):
        self.createTableQuery = self.generateCreateTableQuery()
        try:
            self.conn.execute(self.createTableQuery)
        except:
            print("Create table query execution error.")
        print("Table created succesfully.")
        self.insertTableQuery = self.generateInsertTableQuery()
        for index in self.df.index:
            try:
                self.conn.execute(self.insertTableQuery, [str(rowValue) for rowValue in self.df.loc[index]])
            except:
                print("Insert table query execution error.")
        print("Values inserted successfully into database from Excel.")
        try:
            self.conn.commit()
            self.conn.close()
        except:
            print("Commit/close execution error.")
        return
    def updateDatabase(self):
        id = self.df.columns[0]
        idColumn = self.df
        try:
            self.rows = self.conn.execute("Select * from " + self.tableName)
        except:
            print("Query execution error.")
        for row in self.rows:
            flag0 = 0
            for index in self.df.index:
                if(row[0]==str(self.df.loc[index][0])):
                    idColumn = idColumn.drop(idColumn.loc[idColumn['id']==(int(row[0]))].index)
                    flag0 = 1
                    count = 0
                    for i in self.df.loc[index]:
                        if(str(i)!=row[count]):
                            try:
                                updateTableQuery = "Update " + self.tableName + " set " + self.columnNames[count] + " = '" + str(i) + "' where " + id + " = " + row[0]
                                self.conn.execute(updateTableQuery)
                            except:
                                print("Update table query execution error.")
                        count += 1
            if(flag0==0):
                try:
                    deleteTableQuery = "Delete from " + self.tableName + " where " + id + " = " + row[0]
                    self.conn.execute(deleteTableQuery)
                except:
                    print("Delete table query execution error.")
        for index in idColumn.index:
            try:
                self.insertTableQuery = self.generateInsertTableQuery()
                self.conn.execute(self.insertTableQuery, [str(rowValue) for rowValue in idColumn.loc[index]])
            except:
                continue
        try:
            self.conn.commit()
            self.conn.close()
        except:
            print("Commit/close execution error.")
        return
    def sqlToExcel(self):
        self.rows = self.conn.execute("Select * from " + self.tableName)
        list0 = []
        list0.append(self.columnNames)
        for row in self.rows:
            list0.append(list(row))
        df = pd.DataFrame(list0[1:], columns = list0[0])
        df.to_excel(self.fileName, index = False)
        return