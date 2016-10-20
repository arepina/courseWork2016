import sqlite3


class DataBase:
    conn = None  # database
    c = None  # cursor
    dbName = 'Review.db'

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
    def add_review(self, category_name, subcategory_name, compcategory_name, review_id, rewiew_pro, review_text, agree, date):
        self.c.execute(
            'INSERT INTO Review (categoryName, subcategoryName, compcategoryName, reviewId, rewiewPro, reviewText, agree, date) '
            'VALUES (?,?,?,?,?,?,?,?)',
            (category_name, subcategory_name, compcategory_name, review_id, rewiew_pro, review_text, agree, date))
        self.commit()

    # get the review
    def get_review(self, review_id):
        review = self.c.execute('SELECT * FROM Review WHERE reviewId = ' + str(review_id))
        return review.fetchone()

    # delete the review
    def remove_review(self, review_id):
        self.c.execute('DELETE FROM Review WHERE reviewId = ' + str(review_id))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()
