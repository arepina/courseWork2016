import sqlite3


class DataBase_Eldorado:
    conn = None  # database
    c = None  # cursor
    dbName = 'Review_Eldorado.db'

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
             (id INTEGER PRIMARY KEY AUTOINCREMENT, categotyName TEXT, reviewText TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, category_name, review_text):
        self.c.execute(
            'INSERT INTO Review (categotyName, reviewText) '
            'VALUES (?, ?)',
            (category_name, review_text))
        self.commit()

    # get the review
    def get_review(self, review_id):
        review = self.c.execute('SELECT * FROM Review WHERE id = ' + str(review_id))
        return review.fetchone()

    # delete the review
    def remove_review(self, review_id):
        self.c.execute('DELETE FROM Review WHERE id = ' + str(review_id))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()
