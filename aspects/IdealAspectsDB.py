import sqlite3
import os


class IdealAspectsDB:
    conn_aspects = None

    cursor_aspects = None

    db_aspects_name = 'IdealAspects_Ulmart.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.cursor_aspects = self.conn_aspects.cursor()
        self.create_aspects_db()

    # Create table
    def create_aspects_db(self):
        self.cursor_aspects.execute('''CREATE TABLE IF NOT EXISTS IdealAspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.cursor_aspects.execute(
            'INSERT INTO IdealAspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()

    # commit
    def commit(self):
        self.conn_aspects.commit()

