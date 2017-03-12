import sqlite3
import os


class IdealAspectsDB:
    conn_aspects = None

    cursor_aspects = None
    cursor_aspects_update = None

    db_aspects_name = 'IdealAspects_Ulmart.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_aspects_trees = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name_trees)
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_aspects_update = self.conn_aspects.cursor()
        self.cursor_trees = self.conn_aspects_trees.cursor()
        self.create_aspects_db()

    # Create table
    def create_aspects_db(self):
        self.conn_aspects.execute('''CREATE TABLE IF NOT EXISTS IdealAspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects.commit()

    # Insert new review to DB
    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_aspects.execute(
            'INSERT INTO IdealAspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    # destructor - close connection
    def __del__(self):
        self.conn_aspects_trees.close()
        self.conn_aspects.close()

    def remove_duplicates(self):
        row = self.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
        count = 0
        while row is not None:
            print(count)
            count += 1
            article = str(row[0])
            adv = str(row[1])
            dis = str(row[2])
            com = str(row[3])
            new_str = self.process(adv)
            if new_str != adv:
                self.cursor_aspects_update.execute(
                    'UPDATE IdealAspects SET advantageAspects = ? WHERE article = ? AND advantageAspects = ?',
                    (new_str, article, adv,))
                self.conn_aspects.commit()
            new_str = self.process(dis)
            if new_str != dis:
                self.cursor_aspects_update.execute(
                    'UPDATE IdealAspects SET disadvantageAspects = ? WHERE article = ? AND disadvantageAspects = ?',
                    (new_str, article, dis,))
                self.conn_aspects.commit()
            new_str = self.process(com)
            if new_str != com:
                self.cursor_aspects_update.execute(
                    'UPDATE IdealAspects SET commentAspects = ? WHERE article = ? AND commentAspects = ?',
                    (new_str, article, com,))
                self.conn_aspects.commit()
            row = self.cursor_aspects.fetchone()

    @staticmethod
    def process(part):
        if len(part) != 0:
            new_str = ""
            arr = part.split(";")
            for i in range(len(arr)):
                flag = False
                for j in range(i + 1, len(arr)):
                    if arr[i] == arr[j]:
                        flag = True
                if not flag:
                    new_str += arr[i] + ";"
            new_str = new_str[0:len(new_str) - 1]
            return new_str
        return ""

    def count_aspects(self):
        row = self.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
        count = 0
        aspects_num = 0
        while row is not None:
            print(count)
            count += 1
            adv = str(row[1])
            dis = str(row[2])
            com = str(row[3])
            if len(adv) != 0:
                arr = adv.split(";")
                aspects_num += len(arr)
            if len(dis) != 0:
                arr = dis.split(";")
                aspects_num += len(arr)
            if len(com) != 0:
                arr = com.split(";")
                aspects_num += len(arr)
            row = self.cursor_aspects.fetchone()
        print(aspects_num)
