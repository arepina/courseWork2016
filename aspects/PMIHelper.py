import sqlite3


class PMI:
    conn = None
    cursor = None
    cursor_extra = None
    db = 'DataBase_PMIHelper.db'
    conn_ideal = None
    cursor_ideal = None
    db_ideal = 'IdealAspects_Ulmart.db'

    def __init__(self):
        import os
        path = os.getcwd()
        self.conn = sqlite3.connect(path + "\\..\\db\\" + self.db)
        self.cursor = self.conn.cursor()
        self.cursor_extra = self.conn.cursor()
        self.conn_ideal = sqlite3.connect(path + "\\..\\db\\" + self.db_ideal)
        self.cursor_ideal = self.conn_ideal.cursor()
        self.create_db()

    def create_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PMIHelper
                 (article INT, aspect TEXT, numberInReview INT)''')
        self.commit()

    def __del__(self):
        self.conn.close()

    # commit
    def commit(self):
        self.conn.commit()

    def calculate(self):
        row_aspect = self.cursor_ideal.execute('SELECT * FROM IdealAspects').fetchone()
        count = 0
        while row_aspect is not None:
            print(count)
            count += 1
            article = str(row_aspect[0])
            adv = str(row_aspect[1])
            dis = str(row_aspect[2])
            com = str(row_aspect[3])
            self.process(adv + ";" + dis + ";" + com, article)
            row_aspect = self.cursor_ideal.fetchone()

    def process(self, review, article):
        aspects = review.split(";")
        dict = {}
        for asp in aspects:
            if len(asp) != 0:
                if asp not in dict:
                    dict[asp] = 1
                else:
                    dict[asp] += 1
        for item in dict:
            self.cursor.execute(
                    'INSERT INTO PMIHelper (article, aspect, numberInReview) VALUES (?, ?,  ?)',
                    (article, item, dict[item],))
            self.commit()





# pmi = PMI()
# pmi.calculate()
import nltk
from nltk.collocations import *
from nltk.tokenize import word_tokenize

text = "this is a foo bar bar black sheep  foo bar bar black sheep foo bar bar black sheep shep bar bar black sentence"
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(word_tokenize(text))
for i in finder.score_ngrams(bigram_measures.pmi):
    print(i)
