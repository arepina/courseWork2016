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
    conn_semantic_distance_ideal = None
    conn_local_context_prepare = None
    conn_global_context_prepare = None
    conn_global_context_prepare_extra = None
    conn_global_context = None
    conn_local_context = None
    conn_lexical = None
    conn_lexical_ideal = None
    conn_syntactic = None
    conn_syntactic_ideal = None
    conn_tree = None
    conn_local_context_ideal = None
    conn_global_context_ideal = None
    conn_hierarchy = None

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
    cursor_semantic_distance_ideal = None
    cursor_local_context_prepare = None
    cursor_global_context_prepare = None
    cursor_global_context_prepare_extra = None
    cursor_global_context = None
    cursor_local_context_ideal = None
    cursor_global_context_ideal = None
    cursor_local_context = None
    cursor_lexical = None
    cursor_lexical_ideal = None
    cursor_syntactic = None
    cursor_syntactic_ideal = None
    cursor_tree = None
    cursor_hierarchy = None

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
    db_semantic_distance_ideal = "Semantic_Distance_Ideal.db"
    db_local_context_prepare = "Local_Context_Prepare.db"
    db_global_context_prepare = "Global_Context_Prepare.db"
    db_global_context_prepare_extra = "Global_Context_Prepare_Extra.db"
    db_global_context = "Global_Context.db"
    db_local_context = "Local_Context.db"
    db_lexical = "Lexical.db"
    db_lexical_ideal = "Lexical_Ideal.db"
    db_syntactic = "Syntactic.db"
    db_syntactic_ideal = "Syntactic_Ideal.db"
    db_tree = "Tree.db"
    db_local_context_ideal = "Local_Context_Ideal.db"
    db_global_context_ideal = "Global_Context_Ideal.db"
    db_hierarchy = "Hierarchy.db"

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
        self.conn_semantic_distance_ideal = sqlite3.connect(path + "/../db/" + self.db_semantic_distance_ideal)
        self.conn_local_context_prepare = sqlite3.connect(path + "/../db/" + self.db_local_context_prepare)
        self.conn_global_context_prepare = sqlite3.connect(path + "/../db/" + self.db_global_context_prepare)
        self.conn_global_context_prepare_extra = sqlite3.connect(path + "/../db/" + self.db_global_context_prepare_extra)
        self.conn_global_context = sqlite3.connect(path + "/../db/" + self.db_global_context)
        self.conn_local_context = sqlite3.connect(path + "/../db/" + self.db_local_context)
        self.conn_lexical = sqlite3.connect(path + "/../db/" + self.db_lexical)
        self.conn_syntactic = sqlite3.connect(path + "/../db/" + self.db_syntactic)
        self.conn_tree = sqlite3.connect(path + "/../db/" + self.db_tree)
        self.conn_lexical_ideal = sqlite3.connect(path + "/../db/" + self.db_lexical_ideal)
        self.conn_syntactic_ideal = sqlite3.connect(path + "/../db/" + self.db_syntactic_ideal)
        self.conn_local_context_ideal = sqlite3.connect(path + "/../db/" + self.db_local_context_ideal)
        self.conn_global_context_ideal = sqlite3.connect(path + "/../db/" + self.db_global_context_ideal)
        self.conn_hierarchy = sqlite3.connect(path + "/../db/" + self.db_hierarchy)

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
        self.cursor_semantic_distance_ideal = self.conn_semantic_distance_ideal.cursor()
        self.cursor_local_context_prepare = self.conn_local_context_prepare.cursor()
        self.cursor_global_context_prepare = self.conn_global_context_prepare.cursor()
        self.cursor_global_context_prepare_extra = self.conn_global_context_prepare_extra.cursor()
        self.cursor_global_context = self.conn_global_context.cursor()
        self.cursor_local_context = self.conn_local_context.cursor()
        self.cursor_lexical = self.conn_lexical.cursor()
        self.cursor_lexical_ideal = self.conn_lexical_ideal.cursor()
        self.cursor_syntactic = self.conn_syntactic.cursor()
        self.cursor_tree = self.conn_tree.cursor()
        self.cursor_syntactic_ideal = self.conn_syntactic_ideal.cursor()
        self.cursor_local_context_ideal = self.conn_local_context_ideal.cursor()
        self.cursor_global_context_ideal = self.conn_global_context_ideal.cursor()
        self.cursor_hierarchy = self.conn_hierarchy.cursor()


    def create_hierarchy_db(self):
        self.cursor_hierarchy.execute('''CREATE TABLE IF NOT EXISTS Hierarchy (parent TEXT, child TEXT)''')
        self.conn_hierarchy.commit()

    def create_context_global_ideal_db(self):
        self.cursor_global_context_ideal.execute('''CREATE TABLE IF NOT EXISTS Context (aspect1 TEXT, aspect2 TEXT, kl_divergence DOUBLE)''')
        self.conn_global_context_ideal.commit()

    def create_context_local_ideal_db(self):
        self.cursor_local_context_ideal.execute('''CREATE TABLE IF NOT EXISTS Context (aspect1 TEXT, aspect2 TEXT, kl_divergence DOUBLE)''')
        self.conn_local_context_ideal.commit()

    def create_tree_db(self):
        self.cursor_tree.execute('''CREATE TABLE IF NOT EXISTS Tree (sentence TEXT, tree TEXT)''')
        self.conn_tree.commit()

    def create_syntactic_ideal_db(self):
        self.cursor_syntactic_ideal.execute('''CREATE TABLE IF NOT EXISTS Syntactic (aspect1 TEXT, aspect2 TEXT, syntactic_path INT)''')
        self.conn_syntactic_ideal.commit()

    def create_syntactic_db(self):
        self.cursor_syntactic.execute('''CREATE TABLE IF NOT EXISTS Syntactic (aspect1 TEXT, aspect2 TEXT, syntactic_path INT)''')
        self.conn_syntactic.commit()

    def create_lexical_db(self):
        self.cursor_lexical.execute('''CREATE TABLE IF NOT EXISTS Lexical (aspect1 TEXT, aspect2 TEXT, length_difference INT)''')
        self.conn_lexical.commit()

    def create_lexical_ideal_db(self):
        self.cursor_lexical_ideal.execute('''CREATE TABLE IF NOT EXISTS Lexical (aspect1 TEXT, aspect2 TEXT, length_difference INT)''')
        self.conn_lexical_ideal.commit()

    def create_context_global_db(self):
        self.cursor_global_context.execute('''CREATE TABLE IF NOT EXISTS Context (aspect1 TEXT, aspect2 TEXT, kl_divergence DOUBLE)''')
        self.conn_global_context.commit()

    def create_context_local_db(self):
        self.cursor_local_context.execute('''CREATE TABLE IF NOT EXISTS Context (aspect1 TEXT, aspect2 TEXT, kl_divergence DOUBLE)''')
        self.conn_local_context.commit()

    def create_context_local_prepare_db(self):
        self.cursor_local_context_prepare.execute('''CREATE TABLE IF NOT EXISTS Context (aspect TEXT, context TEXT)''')
        self.conn_local_context_prepare.commit()

    def create_context_global_prepare_db(self):
        self.cursor_global_context_prepare.execute('''CREATE TABLE IF NOT EXISTS Context (aspect TEXT, review TEXT)''')
        self.conn_global_context_prepare.commit()

    def create_context_global_prepare_extra_db(self):
        self.cursor_global_context_prepare_extra.execute('''CREATE TABLE IF NOT EXISTS Context (aspect TEXT, context TEXT)''')
        self.conn_global_context_prepare_extra.commit()

    def create_semantic_distance_db(self):
        self.cursor_semantic_distance.execute('''CREATE TABLE IF NOT EXISTS Distance (aspect1 TEXT, aspect2 TEXT, distance FLOAT)''')
        self.conn_semantic_distance.commit()

    def create_semantic_distance_ideal_db(self):
        self.cursor_semantic_distance_ideal.execute('''CREATE TABLE IF NOT EXISTS Distance (aspect1 TEXT, aspect2 TEXT, distance FLOAT)''')
        self.conn_semantic_distance_ideal.commit()

    def create_path_weight_db(self):
        self.cursor_path_weight.execute('''CREATE TABLE IF NOT EXISTS Weight (filename TEXT, aspect1 TEXT, aspect2 TEXT, weight INT)''')
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
        self.cursor_sentences_one_word.execute('''CREATE TABLE IF NOT EXISTS Sentences (article TEXT, sentence TEXT)''')
        self.conn_sentences_one_word.commit()

    def create_aspects_db(self):
        self.cursor_aspects.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.conn_aspects.commit()

    def create_sentence_db(self):
        self.cursor_sentence.execute('''CREATE TABLE IF NOT EXISTS Sentences (article TEXT, sentence TEXT)''')
        self.conn_sentence.commit()

    def add_hierarchy(self, parent, child):
        self.cursor_hierarchy.execute('INSERT INTO Hierarchy (parent, child) VALUES (?, ?)', (parent, child))

    def add_tree(self, sentence, tree):
        self.cursor_tree.execute('INSERT INTO Tree (sentence, tree) VALUES (?, ?)', (sentence, tree))

    def add_syntactic_ideal(self, aspect1, aspect2, syntactic_path):
        self.cursor_syntactic_ideal.execute('INSERT INTO Syntactic (aspect1, aspect2, syntactic_path) VALUES (?, ?, ?)',
            (aspect1, aspect2, syntactic_path))

    def add_syntactic(self, aspect1, aspect2, syntactic_path):
        self.cursor_syntactic.execute('INSERT INTO Syntactic (aspect1, aspect2, syntactic_path) VALUES (?, ?, ?)',
            (aspect1, aspect2, syntactic_path))

    def add_lexical(self, aspect1, aspect2, length_difference):
        self.cursor_lexical.execute('INSERT INTO Lexical (aspect1, aspect2, length_difference) VALUES (?, ?, ?)',
            (aspect1, aspect2, length_difference))

    def add_lexical_ideal(self, aspect1, aspect2, length_difference):
        self.cursor_lexical_ideal.execute('INSERT INTO Lexical (aspect1, aspect2, length_difference) VALUES (?, ?, ?)',
            (aspect1, aspect2, length_difference))

    def add_context_global_ideal(self, aspect1, aspect2, kl_divergence):
        self.cursor_global_context_ideal.execute('INSERT INTO Context (aspect1, aspect2, kl_divergence) VALUES (?, ?, ?)',
            (aspect1, aspect2, kl_divergence))

    def add_context_local_ideal(self, aspect1, aspect2, kl_divergence):
        self.cursor_local_context_ideal.execute('INSERT INTO Context (aspect1, aspect2, kl_divergence) VALUES (?, ?, ?)',
            (aspect1, aspect2, kl_divergence))

    def add_context_global(self, aspect1, aspect2, kl_divergence):
        self.cursor_global_context.execute('INSERT INTO Context (aspect1, aspect2, kl_divergence) VALUES (?, ?, ?)',
            (aspect1, aspect2, kl_divergence))

    def add_context_local(self, aspect1, aspect2, kl_divergence):
        self.cursor_local_context.execute('INSERT INTO Context (aspect1, aspect2, kl_divergence) VALUES (?, ?, ?)',
            (aspect1, aspect2, kl_divergence))

    def add_context_local_prepare(self, aspect, context):
        self.cursor_local_context_prepare.execute('INSERT INTO Context (aspect, context) VALUES (?, ?)', (aspect, context))

    def add_context_global_prepare(self, aspect, review):
        self.cursor_global_context_prepare.execute('INSERT INTO Context (aspect, review) VALUES (?, ?)', (aspect, review))

    def add_context_global_prepare_extra(self, aspect, context):
        self.cursor_global_context_prepare_extra.execute('INSERT INTO Context (aspect, context) VALUES (?, ?)',
            (aspect, context))

    def add_semantic_distance_ideal(self, aspect1, aspect2, distance):
        self.cursor_semantic_distance_ideal.execute('INSERT INTO Distance (aspect1, aspect2, distance) VALUES (?, ?, ?)',
            (aspect1, aspect2, distance))

    def add_semantic_distance(self, aspect1, aspect2, distance):
        self.cursor_semantic_distance.execute('INSERT INTO Distance (aspect1, aspect2, distance) VALUES (?, ?, ?)',
            (aspect1, aspect2, distance))

    def add_path_weight(self, filename, aspect1, aspect2, weight):
        self.cursor_path_weight.execute('INSERT INTO Weight (filename, aspect1, aspect2, weight) VALUES (?, ?, ?, ?)',
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
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_aspects(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_aspects_one_word.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.conn_reviews_one_word.execute(
            'INSERT INTO Reviews (article, advantageAspects, disadvantageAspects, commentAspects) VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))

    def add_one_word_sentence(self, article, sentence):
        self.conn_sentences_one_word.execute('INSERT INTO Sentences (article, sentence) VALUES (?, ?)',
            (article, sentence))

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()
        self.conn_reviews.close()

    def delete_aspects(self, article):
        self.cursor_aspects.execute('DELETE FROM Aspects WHERE article = ' + str(article))
        self.conn_aspects.commit()
