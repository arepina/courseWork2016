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
    conn_path_weight = None
    conn_semantic_distance = None
    conn_context = None
    conn_global_context = None
    conn_local_context = None

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
    cursor_path_weight = None
    cursor_semantic_distance = None
    cursor_context = None
    cursor_global_context = None
    cursor_local_context = None

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
    db_path_weight = "Path_Weight.db"
    db_semantic_distance = "Semantic_Distance.db"
    db_context = "Context.db"
    db_global_context = "Global_Context.db"
    db_local_context = "Local_Context.db"

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "/../db/" + self.db_aspects_name)
        self.conn_reviews = sqlite3.connect(path + "/../db/" + self.db_reviews_name)
        self.conn_merged = sqlite3.connect(path + "/../db/" + self.db_merged_name)
        self.conn_sentence = sqlite3.connect(path + "/../db/" + self.db_sentence_name)
        self.conn_aspects_one_word = sqlite3.connect(path + "/../db/" + self.db_aspects_one_word_name)
        self.conn_reviews_one_word = sqlite3.connect(path + "/../db/" + self.db_reviews_one_word_name)
        self.conn_sentences_one_word = sqlite3.connect(path + "/../db/" + self.db_sentences_one_word_name)
        self.cursor_sentences_one_word_update = sqlite3.connect(path + "/../db/" + self.db_sentences_one_word_name)
        self.conn_pmi_review = sqlite3.connect(path + "/../db/" + self.db_pmi_review_name)
        self.conn_pmi_sentence = sqlite3.connect(path + "/../db/" + self.db_pmi_sentence_name)
        self.conn_pmi_ideal_review = sqlite3.connect(path + "/../db/" + self.db_pmi_ideal_review_name)
        self.conn_pmi_ideal_sentence = sqlite3.connect(path + "/../db/" + self.db_pmi_ideal_sentence_name)
        self.conn_path_weight = sqlite3.connect(path + "/../db/" + self.db_path_weight)
        self.conn_semantic_distance = sqlite3.connect(path + "/../db/" + self.db_semantic_distance)
        self.conn_context = sqlite3.connect(path + "/../db/" + self.db_context)
        self.conn_global_context = sqlite3.connect(path + "/../db/" + self.db_global_context)
        self.conn_local_context = sqlite3.connect(path + "/../db/" + self.db_local_context)

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
        self.cursor_path_weight = self.conn_path_weight.cursor()
        self.cursor_semantic_distance = self.conn_semantic_distance.cursor()
        self.cursor_context = self.conn_context.cursor()
        self.cursor_global_context = self.conn_global_context.cursor()
        self.cursor_local_context = self.conn_local_context.cursor()

    def create_context_global_db(self):
        self.cursor_global_context.execute('''CREATE TABLE IF NOT EXISTS Context
                        (aspect1 TEXT, aspect2 TEXT, kl_divergence DOUBLE)''')
        self.conn_global_context.commit()

    def create_context_local_db(self):
        self.cursor_local_context.execute('''CREATE TABLE IF NOT EXISTS Context
                        (review_num INT, aspect TEXT, ngram TEXT)''')
        self.conn_local_context.commit()

    def create_context_db(self):
        self.cursor_context.execute('''CREATE TABLE IF NOT EXISTS Context
                        (aspect TEXT, context TEXT)''')
        self.conn_context.commit()

    def create_semantic_distance_db(self):
        self.cursor_semantic_distance.execute('''CREATE TABLE IF NOT EXISTS Distance
                (aspect1 TEXT, aspect2 TEXT, distance INT)''')
        self.conn_semantic_distance.commit()

    def create_path_weight_db(self):
        self.cursor_path_weight.execute('''CREATE TABLE IF NOT EXISTS Weight
             (filename TEXT, aspect1 TEXT, aspect2 TEXT, weight INT)''')
        self.conn_path_weight.commit()

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

    def add_context_global(self, aspect1, aspect2, kl_divergence):
        self.cursor_global_context.execute(
            'INSERT INTO Context (aspect1, aspect2, kl_divergence) VALUES (?, ?, ?)',
            (aspect1, aspect2, kl_divergence))

    def add_context_local(self, review_num, aspect, ngram):
        self.cursor_local_context.execute(
            'INSERT INTO Context (review_num, aspect, ngram) VALUES (?, ?, ?)',
            (review_num, aspect, ngram))

    def add_context(self, aspect, context):
        self.cursor_context.execute(
            'INSERT INTO Context (aspect, context) VALUES (?, ?)',
            (aspect, context))

    def add_semantic_distance(self, aspect1, aspect2, distance):
        self.cursor_semantic_distance.execute(
            'INSERT INTO Distance (aspect1, aspect2, distance) VALUES (?, ?, ?)',
            (aspect1, aspect2, distance))

    def add_path_weight(self, filename, aspect1, aspect2, weight):
        self.cursor_path_weight.execute(
            'INSERT INTO Weight (filename, aspect1, aspect2, weight) VALUES (?, ?, ?, ?)',
            (filename, aspect1, aspect2, weight))

    def add_pmi_ideal_review(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_ideal_review.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))

    def add_pmi_ideal_sentence(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_ideal_sentence.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))

    def add_pmi_review(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_review.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))

    def add_pmi_sentence(self, aspect1, aspect2, num1, num2, both_num, pmi):
        self.cursor_pmi_sentence.execute(
            'INSERT INTO PMI (aspect1, aspect2, aspect1Num, aspect2Num, bothNum, pmi) VALUES (?, ?, ?, ?, ?, ?)',
            (aspect1, aspect2, num1, num2, both_num, pmi))

    def add_sentence(self, article, sentence):
        self.cursor_sentence.execute('INSERT INTO Sentences (article, sentence) VALUES (?, ?)', (article, sentence))

    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.cursor_aspects.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_aspects(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_aspects_one_word.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_reviews_one_word.execute(
            'INSERT INTO Reviews (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_sentence(self, article, sentence):
        self.conn_sentences_one_word.execute(
            'INSERT INTO Sentences (article, sentence) '
            'VALUES (?, ?)',
            (article, sentence))

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()
        self.conn_reviews.close()

    def delete_aspects(self, article):
        self.cursor_aspects.execute('DELETE FROM Aspects WHERE article = ' + str(article))
        self.conn_aspects.commit()
