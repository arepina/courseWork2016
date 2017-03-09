import json
from datetime import datetime
from operator import itemgetter

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from aspects.Aspects import Aspects
from aspects.PMI import PMI

import re


class Syntactic:
    def process(self, db, vocabulary, aspect_class_object):
        db.create_syntactic_db()
        # db.create_tree_db()  # load syntactic trees from api ispras
        corpus = PMI.get_all_sentences_corpus(db)
        # self.build_tree(corpus, aspect_class_object, db)
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        col_array = PMI.create_col_array(matrix, len(matrix_terms))
        col_array = np.array(col_array)
        for i in range(len(matrix_terms)):
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                print(j)
                col1 = col_array[i]
                col2 = col_array[j]
                non_zero_sentences_indexes = np.nonzero(col1 * col2)[1]
                if len(non_zero_sentences_indexes) == 0:  # independent
                    syntactic = -1
                else:
                    non_zero_sentences = itemgetter(*non_zero_sentences_indexes)(corpus)
                    if len(non_zero_sentences_indexes) == 1:
                        syntactic = self.find_path_for_sentence(non_zero_sentences, matrix_terms[i], matrix_terms[j], 0,
                                                                1, db)
                    else:
                        syntactic = self.calculate_syntactic(matrix_terms[i], matrix_terms[j], non_zero_sentences, db)
                db.add_syntactic(matrix_terms[i], matrix_terms[j], syntactic)
            print(datetime.now() - start)
            if i % 100 == 0:
                db.conn_syntactic.commit()
        db.conn_syntactic.commit()

    def process_ideal(self, db):
        db.create_syntactic_ideal_db()
        corpus = PMI.get_all_sentences_corpus(db)
        row_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        vocabulary = []
        while row_ideal is not None:
            aspect1 = str(row_ideal[0])
            aspect2 = str(row_ideal[1])
            if aspect1 not in vocabulary:
                vocabulary.append(aspect1)
            if aspect2 not in vocabulary:
                vocabulary.append(aspect2)
            row_ideal = db.cursor_pmi_ideal_review.fetchone()
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        col_array = PMI.create_col_array(matrix, len(matrix_terms))
        for i in range(len(matrix_terms)):
            print(i)
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                print(j)
                col1 = col_array[i]
                col2 = col_array[j]
                non_zero_sentences_indexes = np.nonzero(col1 * col2)[1]
                if len(non_zero_sentences_indexes) == 0:  # independent
                    syntactic = -1
                else:
                    non_zero_sentences = itemgetter(*non_zero_sentences_indexes)(corpus)
                    if len(non_zero_sentences_indexes) == 1:
                        syntactic = self.find_path_for_sentence(non_zero_sentences, matrix_terms[i], matrix_terms[j], 0,
                                                                1, db)
                    else:
                        syntactic = self.calculate_syntactic(matrix_terms[i], matrix_terms[j], non_zero_sentences, db)
                db.add_syntactic_ideal(matrix_terms[i], matrix_terms[j], syntactic)
            print(datetime.now() - start)
            db.conn_syntactic_ideal.commit()

    def calculate_syntactic(self, aspect1, aspect2, non_zero_sentences, db):
        divider = len(non_zero_sentences)
        syntactic_paths_sum = 0
        dict = {}
        for sentence in non_zero_sentences:
            if sentence in dict:
                syntactic_paths_sum += dict[sentence]
            else:
                sum_before = syntactic_paths_sum
                syntactic_paths_sum = self.find_path_for_sentence(sentence, aspect1, aspect2, syntactic_paths_sum, divider,
                                                                  db)
                dict[sentence] = syntactic_paths_sum - sum_before
        return syntactic_paths_sum / divider

    def find_path(self, aspect1, aspect2, aspect1_parent, aspect2_parent, syntax_relations, aspect1_parents,
                  aspect2_parents):
        while True:
            if aspect1_parents[len(aspect1_parents) - 1] == aspect2_parents[
                        len(aspect2_parents) - 1]:  # aspect parents have just intersected
                return len(aspect1_parents) + len(aspect2_parents)
            if aspect2_parent in aspect1_parents:  # next aspect2 parent has intersection with list of aspect1 parents
                index = aspect1_parents.index(aspect2_parent) + 1
                return index + len(aspect2_parents)
            if aspect1_parent in aspect2_parents:  # next aspect1 parent has intersection with list of aspect2 parents
                index = aspect2_parents.index(aspect1_parent) + 1
                return index + len(aspect1_parents)
            if aspect1_parent == aspect2:  # the next aspect1 parent is out aspect2
                return len(aspect1_parents)
            if aspect2_parent == aspect1:  # the next aspect2 parent is out aspect1
                return len(aspect2_parents)
            if aspect1_parent == "" and aspect2_parent == "":  # the words don't have intersection at all
                return max(len(aspect1_parents), len(aspect2_parents))
            try:
                if aspect1_parent != "":
                    aspect1_parent = self.get_parent(aspect1_parent, syntax_relations)["value"]["parent"]["start"]
                    aspect1_parents.append(aspect1_parent)
            except:
                aspect1_parent = ""  # there is no next parent
            try:
                if aspect2_parent != "":
                    aspect2_parent = self.get_parent(aspect2_parent, syntax_relations)["value"]["parent"]["start"]
                    aspect2_parents.append(aspect2_parent)
            except:
                aspect2_parent = ""  # there is no next parent

    @staticmethod
    def get_parent(start_index, syntax_relations):
        for relation in syntax_relations:
            if start_index == relation["start"]:
                return relation

    def find_path_for_sentence(self, sentence, aspect1, aspect2, syntactic_paths_sum, divider, db):
        row_syntactic_tree = db.cursor_tree.execute('SELECT * FROM Tree WHERE sentence = ?', (sentence,)).fetchone()
        data = json.loads(str(row_syntactic_tree[1]))
        aspect_error_happened = False
        syntax_relations = data['annotations']['syntax-relation']
        try:
            aspect1_start_index = re.search(r'\b(%s)\b' % aspect1, sentence).start()
        except:
            aspect1_start_index = 0
            aspect_error_happened = True
        try:
            aspect2_start_index = re.search(r'\b(%s)\b' % aspect2, sentence).start()
        except:
            aspect2_start_index = 0
            aspect_error_happened = True
        aspect1_parents = []
        aspect2_parents = []
        try:
            aspect1_parent = self.get_parent(aspect1_start_index, syntax_relations)["value"]["parent"]["start"]
        except:
            aspect1_parent = aspect1_start_index - 1  # trying to fix the error later in method
        aspect1_parents.append(aspect1_parent)
        try:
            aspect2_parent = self.get_parent(aspect2_start_index, syntax_relations)["value"]["parent"]["start"]
        except:
            aspect2_parent = aspect2_start_index - 1  # trying to fix the error later in method
        aspect2_parents.append(aspect2_parent)
        if aspect1_parent == aspect2_start_index or aspect2_parent == aspect1_start_index:
            if not aspect_error_happened:  # one aspect is parent to another
                syntactic_paths_sum += 1
            else:
                divider -= 1
        else:
            if not aspect_error_happened:  # don't need the results which was incorrectly included because of sklearn lib
                syntactic_paths_sum += self.find_path(aspect1_start_index, aspect2_start_index, aspect1_parent,
                                                      aspect2_parent, syntax_relations, aspect1_parents,
                                                      aspect2_parents)
            else:
                divider -= 1
        return syntactic_paths_sum

    @staticmethod
    def build_tree(sentences, aspect_class_object, db):
        for sentence in sentences:
            row_sentence = db.cursor_tree.execute('SELECT * FROM Tree WHERE sentence = ?', (sentence,)).fetchone()
            if row_sentence is None:  # the sentence is not in db
                syntactic_tree = Aspects.syntatic_parsing(sentence, aspect_class_object)
                db.add_tree(sentence, syntactic_tree)
            db.conn_tree.commit()
