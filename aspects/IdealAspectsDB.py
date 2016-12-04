import sqlite3
import os


class IdealAspectsDB:
    conn_aspects = None
    conn_aspects_trees = None

    cursor_aspects = None
    cursor_aspects2 = None
    cursor_trees = None

    db_aspects_name_trees = 'IdealAspects_Trees.db'
    db_aspects_name = 'IdealAspects_Ulmart.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_aspects_trees = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name_trees)
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_aspects2 = self.conn_aspects.cursor()
        self.cursor_trees = self.conn_aspects_trees.cursor()
        self.create_aspects_db()

    # Create table
    def create_aspects_db(self):
        self.conn_aspects_trees.execute('''CREATE TABLE IF NOT EXISTS IdealAspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_aspects_trees.execute(
            'INSERT INTO IdealAspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn_aspects_trees.close()
        self.conn_aspects.close()

    # commit
    def commit(self):
        self.conn_aspects_trees.commit()

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
                self.cursor_aspects2.execute('UPDATE IdealAspects SET advantageAspects = ? WHERE article = ? and advantageAspects = ?', (new_str, article, adv,))
                self.commit()

            new_str = self.process(dis)
            if new_str != dis:
                self.cursor_aspects2.execute('UPDATE IdealAspects SET disadvantageAspects = ? WHERE article = ? and disadvantageAspects = ?', (new_str, article, dis,))
                self.commit()

            new_str = self.process(com)
            if new_str != com:
                self.cursor_aspects2.execute('UPDATE IdealAspects SET commentAspects = ? WHERE article = ? and commentAspects = ?', (new_str, article, com,))
                self.commit()
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
        row = self.cursor_trees.execute('SELECT * FROM IdealAspects').fetchone()
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
            row = self.cursor_trees.fetchone()
        print(aspects_num)

i = IdealAspectsDB()
i.count_aspects()