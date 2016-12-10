import sqlite3
import os


class DB:
    conn_aspects = None
    conn_reviews = None
    conn_merged = None
    conn_sentence = None
    conn_aspects_one_word = None
    conn_reviews_one_word = None

    cursor_aspects = None
    cursor_aspects2 = None
    cursor_reviews = None
    cursor_article = None
    cursor_merged = None
    cursor_sentence = None
    cursor_aspects_one_word = None
    cursor_reviews_one_word = None

    db_merged_name = 'Merged.db'
    db_aspects_name = 'Aspects.db'
    db_reviews_name = 'Reviews.db'
    db_sentence_name = 'Sentence.db'
    db_aspects_one_word_name = 'Aspects_One_Word.db'
    db_reviews_one_word_name = 'Reviews_One_Word.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_reviews = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_name)
        self.conn_merged = sqlite3.connect(path + "\\..\\db\\" + self.db_merged_name)
        self.conn_sentence = sqlite3.connect(path + "\\..\\db\\" + self.db_sentence_name)
        self.conn_aspects_one_word = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_one_word_name)
        self.conn_reviews_one_word = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_one_word_name)

        self.cursor_merged = self.conn_merged.cursor()
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_aspects2 = self.conn_aspects.cursor()
        self.cursor_reviews = self.conn_reviews.cursor()
        self.cursor_article = self.conn_aspects.cursor()
        self.cursor_sentence = self.conn_sentence.cursor()
        self.cursor_aspects_one_word = self.conn_aspects_one_word.cursor()
        self.cursor_reviews_one_word = self.conn_reviews_one_word.cursor()

    def create_aspects_one_word_db(self):
        self.cursor_aspects_one_word.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects_one_word.commit()

    def create_reviews_one_word_db(self):
        self.cursor_reviews_one_word.execute('''CREATE TABLE IF NOT EXISTS Reviews
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_reviews_one_word.commit()

    def create_aspects_db(self):
        self.cursor_aspects.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects.commit()

    def create_sentence_db(self):
        self.cursor_sentence.execute('''CREATE TABLE IF NOT EXISTS Sentences
             (article TEXT, sentence TEXT)''')
        self.conn_sentence.commit()

    def add_sentence(self, article, sentence):
        self.cursor_sentence.execute('INSERT INTO Sentences (article, sentence) VALUES (?, ?)',(article, sentence))
        self.conn_sentence.commit()

    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.cursor_aspects.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.conn_aspects.commit()

    def add_one_word_aspects(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_aspects_one_word.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.conn_aspects_one_word.commit()

    def add_one_word_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_reviews_one_word.execute(
            'INSERT INTO Reviews (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.conn_reviews_one_word.commit()

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()
        self.conn_reviews.close()

    def delete_aspects(self, article):
        self.cursor_aspects.execute('DELETE FROM Aspects WHERE article = ' + str(article))
        self.conn_aspects.commit()

