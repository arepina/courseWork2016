import pypyodbc
import sqlite3


class Azure:
    connectionAzure = None
    connectionLocal = None
    cursorLocal = None
    cursorAzure = None
    dbName = 'Review_Ulmart.db'

    def __init__(self):
        import os
        path = os.getcwd()
        self.connectionLocal = sqlite3.connect(path + "\\..\\db\\" + self.dbName)
        self.cursorLocal = self.connectionLocal.cursor()
        self.connectionAzure = pypyodbc.connect(
            'Driver={ODBC Driver 13 for SQL Server};Server=tcp:ulmart.database.windows.net,1433;Database=Ulmart;Uid=anastasia@ulmart;Pwd=12345678Qwerty;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        #'Driver={ODBC Driver 13 for SQL Server};Server=tcp:ulmart.database.windows.net,1433;Database=Ulmart;Uid=anastasia@ulmart;Pwd={12345678Qwerty};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        self.cursorAzure = self.connectionAzure.cursor()


    def upload(self):
        self.cursorLocal.execute("SELECT * FROM Review")
        row = self.cursorLocal.fetchone()
        while row is not None:
            print(row)
            sql_command = ('INSERT INTO Ulmart '
                           '(category_name, subcategory_name, article, advantage, disadvantage, comment) '
                           'VALUES (?,?,?,?,?,?)')
            values = [row[0], row[1], row[2], row[3], row[4], row[5]]
            self.cursorAzure.execute(sql_command, values)
            row = self.cursorLocal.fetchone()


azureConnection = Azure()
azureConnection.upload()
azureConnection.connectionAzure.commit()
azureConnection.connectionAzure.close()
