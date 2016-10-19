import sqlite3


class DataBase:
    conn = None  # database
    c = None  # cursor
    dbName = 'Review.db'

    # constructor
    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\" + self.dbName)
        self.c = self.conn.cursor()
        self.create_db()

    # Create table
    def create_db(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Review
             (categoryName TEXT,
             subcategoryName TEXT,
             compcategoryName TEXT,
             reviewId INTEGER PRIMARY KEY,
             rewiewPro TEXT,
             reviewText TEXT,
             agree INTEGER,
             date TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, categoryName, subcategoryName, compcategoryName, reviewId, rewiewPro, reviewText, agree, date):
        self.c.execute(
            'INSERT INTO Review (categoryName, subcategoryName, compcategoryName, reviewId, rewiewPro, reviewText, agree, date) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (categoryName, subcategoryName, compcategoryName, reviewId, rewiewPro, reviewText, agree, date))
        self.commit()

    # get the review
    def get_review(self, reviewId):
        review = self.c.execute('SELECT * FROM Review WHERE reviewId = ' + str(reviewId))
        return review.fetchone()

    # delete the review
    def remove_review(self, reviewId):
        self.c.execute('DELETE FROM Review WHERE reviewId = ' + str(reviewId))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()
