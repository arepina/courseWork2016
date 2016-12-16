import sqlite3
import os


class DB:
    conn_aspects = None
    conn_reviews = None
    conn_merged = None
    conn_sentence = None
    conn_aspects_one_word = None
    conn_reviews_one_word = None
    conn_sentences_one_word = None
    conn_pmi_review = None
    conn_pmi_sentence = None
    conn_pmi_ideal_review = None
    conn_pmi_ideal_sentence = None

    cursor_aspects = None
    cursor_aspects2 = None
    cursor_reviews = None
    cursor_article = None
    cursor_merged = None
    cursor_sentence = None
    cursor_aspects_one_word = None
    cursor_reviews_one_word = None
    cursor_reviews_one_word_update = None
    cursor_sentences_one_word = None
    cursor_sentences_one_word_update = None
    cursor_pmi_review = None
    cursor_pmi_sentence = None
    cursor_pmi_ideal_review = None
    cursor_pmi_ideal_sentence = None

    db_merged_name = 'Merged.db'
    db_aspects_name = 'Aspects.db'
    db_reviews_name = 'Reviews.db'
    db_sentence_name = 'Sentence.db'
    db_aspects_one_word_name = 'Aspects_One_Word.db'
    db_reviews_one_word_name = 'Reviews_One_Word.db'
    db_sentences_one_word_name = 'Sentences_One_Word.db'
    db_pmi_review_name = 'PMI_Review.db'
    db_pmi_sentence_name = 'PMI_Sentence.db'
    db_pmi_ideal_review_name = 'PMI_Ideal_Review.db'
    db_pmi_ideal_sentence_name = 'PMI_Ideal_Sentence.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_reviews = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_name)
        self.conn_merged = sqlite3.connect(path + "\\..\\db\\" + self.db_merged_name)
        self.conn_sentence = sqlite3.connect(path + "\\..\\db\\" + self.db_sentence_name)
        self.conn_aspects_one_word = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_one_word_name)
        self.conn_reviews_one_word = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_one_word_name)
        self.conn_sentences_one_word = sqlite3.connect(path + "\\..\\db\\" + self.db_sentences_one_word_name)
        self.cursor_sentences_one_word_update = sqlite3.connect(path + "\\..\\db\\" + self.db_sentences_one_word_name)
        self.conn_pmi_review = sqlite3.connect(path + "\\..\\db\\" + self.db_pmi_review_name)
        self.conn_pmi_sentence = sqlite3.connect(path + "\\..\\db\\" + self.db_pmi_sentence_name)
        self.conn_pmi_ideal_review = sqlite3.connect(path + "\\..\\db\\" + self.db_pmi_ideal_review_name)
        self.conn_pmi_ideal_sentence = sqlite3.connect(path + "\\..\\db\\" + self.db_pmi_ideal_sentence_name)

        self.cursor_merged = self.conn_merged.cursor()
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_aspects2 = self.conn_aspects.cursor()
        self.cursor_reviews = self.conn_reviews.cursor()
        self.cursor_article = self.conn_aspects.cursor()
        self.cursor_sentence = self.conn_sentence.cursor()
        self.cursor_aspects_one_word = self.conn_aspects_one_word.cursor()
        self.cursor_reviews_one_word = self.conn_reviews_one_word.cursor()
        self.cursor_reviews_one_word_update = self.conn_reviews_one_word.cursor()
        self.cursor_sentences_one_word = self.conn_sentences_one_word.cursor()
        self.cursor_pmi_review = self.conn_pmi_review.cursor()
        self.cursor_pmi_sentence = self.conn_pmi_sentence.cursor()
        self.cursor_pmi_ideal_review = self.conn_pmi_ideal_review.cursor()
        self.cursor_pmi_ideal_sentence = self.conn_pmi_ideal_sentence.cursor()

    def create_pmi_ideal_review_db(self):
        self.cursor_pmi_ideal_review.execute('''CREATE TABLE IF NOT EXISTS PMI
             (aspect1 TEXT, aspect2 TEXT, aspect1Num INT, aspect2Num INT, bothNum INT, pmi DOUBLE)''')
        self.conn_pmi_ideal_review.commit()

    def create_pmi_ideal_sentence_db(self):
        self.cursor_pmi_ideal_sentence.execute('''CREATE TABLE IF NOT EXISTS PMI
             (aspect1 TEXT, aspect2 TEXT, aspect1Num INT, aspect2Num INT, bothNum INT, pmi DOUBLE)''')
        self.conn_pmi_ideal_sentence.commit()

    def create_pmi_review_db(self):
        self.cursor_pmi_review.execute('''CREATE TABLE IF NOT EXISTS PMI
             (aspect1 TEXT, aspect2 TEXT, aspect1Num INT, aspect2Num INT, bothNum INT, pmi DOUBLE)''')
        self.conn_pmi_review.commit()

    def create_pmi_sentence_db(self):
        self.cursor_pmi_sentence.execute('''CREATE TABLE IF NOT EXISTS PMI
             (aspect1 TEXT, aspect2 TEXT, aspect1Num INT, aspect2Num INT, bothNum INT, pmi DOUBLE)''')
        self.conn_pmi_sentence.commit()

    def create_aspects_one_word_db(self):
        self.cursor_aspects_one_word.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects_one_word.commit()

    def create_reviews_one_word_db(self):
        self.cursor_reviews_one_word.execute('''CREATE TABLE IF NOT EXISTS Reviews
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_reviews_one_word.commit()

    def create_sentences_one_word_db(self):
        self.cursor_sentences_one_word.execute('''CREATE TABLE IF NOT EXISTS Sentences
             (article TEXT, sentence TEXT)''')
        self.conn_sentences_one_word.commit()

    def create_aspects_db(self):
        self.cursor_aspects.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects.commit()

    def create_sentence_db(self):
        self.cursor_sentence.execute('''CREATE TABLE IF NOT EXISTS Sentences
             (article TEXT, sentence TEXT)''')
        self.conn_sentence.commit()

    def add_pmi_ideal_review(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_ideal_review.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))
        self.conn_pmi_ideal_review.commit()

    def add_pmi_ideal_sentence(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_ideal_sentence.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))
        self.conn_pmi_ideal_sentence.commit()

    def add_pmi_review(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_review.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))
        self.conn_pmi_review.commit()

    def add_pmi_sentence(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_sentence.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))
        self.conn_pmi_sentence.commit()

    def add_sentence(self, article, sentence):
        self.cursor_sentence.execute('INSERT INTO Sentences (article, sentence) VALUES (?, ?)', (article, sentence))
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

    def add_one_word_sentence(self, article, sentence):
        self.conn_sentences_one_word.execute(
            'INSERT INTO Sentences (article, sentence) '
            'VALUES (?, ?)',
            (article, sentence))
        self.conn_sentences_one_word.commit()

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()
        self.conn_reviews.close()

    def delete_aspects(self, article):
        self.cursor_aspects.execute('DELETE FROM Aspects WHERE article = ' + str(article))
        self.conn_aspects.commit()
