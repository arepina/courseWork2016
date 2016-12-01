import sqlite3


class CategoryNames:
    conn = None  # database
    c = None  # cursor
    dbName = 'Review_Ulmart.db'

    # constructor
    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\..\\db\\" + self.dbName)
        self.c = self.conn.cursor()

    def site_directories_print(self):
        self.c.execute('SELECT DISTINCT category_name FROM Review')
        row = self.c.fetchone()
        while row is not None:
            print(str(row[0]))
            row = self.c.fetchone()

    def sub_categories_print(self):
        self.c.execute('SELECT DISTINCT subcategory_name FROM Review')
        row = self.c.fetchone()
        while row is not None:
            print(str(row[0]))
            self.create(str(row[0]))
            row = self.c.fetchone()

    def create(self, name):
        try:
            name = "D:\courseWork2016\productTrees\Subcategories files\\" + name + ".txt"
            file = open(name, 'a')
            file.close()
        except:
            print("error occured")


category_names = CategoryNames()
category_names.site_directories_print()
category_names.sub_categories_print()
