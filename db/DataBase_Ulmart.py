import sqlite3


class DataBase_Ulmart:
    conn = None  # database
    c = None  # cursor
    dbName = 'Review_Ulmart.db'

    # constructor
    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\..\\db\\" + self.dbName)
        self.c = self.conn.cursor()
        self.create_db()

    # Create table
    def create_db(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Review
             (id INTEGER PRIMARY KEY AUTOINCREMENT, article TEXT, advantage TEXT, disadvantage TEXT, comment TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, article, advantage, disadvantage, comment):
        self.c.execute(
            'INSERT INTO Review (article, advantage, disadvantage, comment) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage, disadvantage, comment))
        self.commit()


    def reviews_num(self, article):
        review_num = self.c.execute('SELECT COUNT(id) FROM Review WHERE Review.article = article GROUP BY Review.article')
        return review_num.fetchone()

    # delete the review
    def remove_review(self, article):
        self.c.execute('DELETE FROM Review WHERE article = ' + str(article))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()
