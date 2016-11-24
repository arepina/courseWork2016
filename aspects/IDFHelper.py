import sqlite3


class IDFHelper:
    conn = None
    cursor = None
    extra_cursor = None
    db = 'DataBase_IDFHelper.db'
    conn_r = None
    cursor_r = None
    db_r = 'Review_Ulmart.db'

    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\..\\db\\" + self.db)
        self.cursor = self.conn.cursor()
        self.extra_cursor = self.conn.cursor()
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

    def cleaner(self):
        self.cursor.execute('SELECT * FROM IDFHelper')
        row = self.cursor.fetchone()
        item = 0
        while row is not None:  # iterate through all reviews
            print(item)
            item += 1
            s = str(row[0])
            #arr = s.split("\n")
            #if(len(arr) > 1):
            if ">" in s or "-" in s or "<" in s:
                new_word = str(row[0]).replace(">", "")
                new_word = new_word.replace("-", "")
                new_word = new_word.replace("<", "")
                new_num = str(row[1])
                n = self.extra_cursor.execute('SELECT number FROM IDFHelper WHERE word = ?', (new_word,)).fetchone()
                if n is None:  # the word is not in db
                    self.extra_cursor.execute('INSERT INTO IDFHelper (word, number) VALUES (?, ?)',(new_word, new_num))
                    self.commit()
                else:  # the word is in db
                    self.extra_cursor.execute(
                    'UPDATE IDFHelper SET number = ? WHERE word = ?', (int(n[0]) + int(new_num), new_word,))
                    self.commit()
                self.extra_cursor.execute('DELETE FROM IDFHelper WHERE word = ?', (str(row[0]),))
                self.commit()
            row = self.cursor.fetchone()


helper = IDFHelper()
helper.cleaner()
#helper.process()
