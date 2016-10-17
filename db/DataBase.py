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
        self.createDB()

    # Create table
    def createDB(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS Review
             (id INTEGER PRIMARY KEY AUTOINCREMENT, review_text TEXT)''')
        self.commit()

    # Insert new review to DB
    def addReview(self, id, review_text):
        self.c.execute('INSERT INTO Review (id, review_text) VALUES (?,?)', (id, review_text))
        self.commit()

    # if review exists
    def isReviewNameExists(self, id, review_text):
        if self.c.execute('SELECT COUNT(*) FROM Review WHERE id = ' + str(
                id) + ' AND review_text = "' + review_text + '"').fetchone()[0] == 0:
            # if review not exists
            return False
        # if review was found
        return True

    # check if the review already exist
    def checkID(self, id):
        if self.getReview(id) is None:
            # if review not exists
            return True
        # if review was found
        return False

    # get the review
    def getReview(self, id):
        review = self.c.execute('SELECT * FROM Review WHERE id = ' + str(id))
        return review.fetchone()

    # delete the review
    def removeReview(self, id):
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()
