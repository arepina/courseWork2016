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
        corpus = PMI.get_all_sentences_corpus(db)
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        count = 0
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        col_array = PMI.create_col_array(matrix, len(matrix_terms))
        # col_array = np.array(col_array)
        for i in range(len(matrix_terms)):
            print(count)
            count += 1
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                col1 = col_array[i]
                col2 = col_array[j]
                non_zero_sentences_indexes = np.nonzero(col1 * col2)[1]
                if len(non_zero_sentences_indexes) == 0:  # independent
                    syntactic = -1
                else:
                    non_zero_sentences = itemgetter(*non_zero_sentences_indexes)(corpus)
                    syntactic = self.calculate_syntactic(matrix_terms[i], matrix_terms[j], non_zero_sentences,
                                                         aspect_class_object)
                db.add_syntactic(matrix_terms[i], matrix_terms[j], syntactic)
            print(datetime.now() - start)
            if count % 1000 == 0:
                db.conn_syntactic.commit()

    def calculate_syntactic(self, aspect1, aspect2, non_zero_sentences, aspect_class_object):
        syntactic_paths_sum = 0
        for sentence in non_zero_sentences:
            syntactic_tree = Aspects.syntatic_parsing(sentence, aspect_class_object)
            data = json.loads(syntactic_tree)
            syntax_relations = data['annotations']['syntax-relation']
            aspect1_start_index = re.search(r'\b(%s)\b' % aspect1, sentence).start()
            aspect2_start_index = re.search(r'\b(%s)\b' % aspect2, sentence).start()
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
            if aspect1_parent == aspect2_start_index or aspect2_parent == aspect1_start_index:  # one aspect is parent to another
                syntactic_paths_sum += 1
            else:
                syntactic_paths_sum += self.find_path(aspect1_start_index, aspect2_start_index, aspect1_parent,
                                                      aspect2_parent, syntax_relations, aspect1_parents,
                                                      aspect2_parents)
        return syntactic_paths_sum / len(non_zero_sentences)

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
