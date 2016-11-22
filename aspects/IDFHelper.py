import sqlite3


class IDFHelper:
    conn = None
    cursor = None
    db = 'DataBase_IDFHelper.db'
    conn_r = None
    cursor_r = None
    db_r = 'Review_Ulmart.db'

    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\..\\db\\" + self.db)
        self.cursor = self.conn.cursor()
        self.conn_r = sqlite3.connect(path + "\\..\\db\\" + self.db_r)
        self.cursor_r = self.conn_r.cursor()
        self.create_db()

    def create_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS IDFHelper
             (word TEXT, number TEXT)''')
        self.commit()

    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()

    def process(self):
        self.cursor_r.execute('SELECT * FROM Review')
        row = self.cursor_r.fetchone()
        while row is not None:  # iterate through all reviews
            print(str(row[2]))
            adv = str(row[3])
            self.counter(adv)
            dis = str(row[4])
            self.counter(dis)
            com = str(row[5])
            self.counter(com)
            row = self.cursor_r.fetchone()

    def counter(self, part):
        words = part.split(" ")
        for word in words:
            word = self.replacer(word).lower()
            n = self.cursor.execute('SELECT number FROM IDFHelper WHERE word = ?', (word,)).fetchone()
            if n is None:  # the word is not in db
                self.cursor.execute('INSERT INTO IDFHelper (word, number) VALUES (?, ?)',(word, 1))
                self.commit()
            else:  # the word is in db
                self.cursor.execute(
                'UPDATE IDFHelper SET number = ? WHERE word = ?', (int(n[0]) + 1, word,))
                self.commit()

    def replacer(self, item):
        item = item.replace(",", "")
        item = item.replace(".", "")
        item = item.replace(";", "")
        item = item.replace("!", "")
        item = item.replace("?", "")
        item = item.replace(")", "")
        item = item.replace("(", "")
        item = item.replace(" ", "")
        return item

helper = IDFHelper()
helper.process()
