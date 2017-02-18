import json
from datetime import datetime

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from aspects.Aspects import Aspects
from aspects.PMI import PMI


class Syntactic:
    def process(self, db, vocabulary, aspect_class_object):
        db.create_syntactic_db()
        corpus = PMI.get_all_sentences_corpus(db)
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        count = 0
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect
        final_matrix = np.array([matrix_terms, matrix_freq])
        col_array = PMI.create_col_array(matrix, len(matrix_terms))
        col_array = np.array(col_array)
        for i in range(len(matrix_terms)):
            print(count)
            count += 1
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                col1 = col_array[i]
                col2 = col_array[j]
                both_num = np.count_nonzero(col1 * col2)
                if both_num == 0:  # independent
                    syntactic = -1
                else:
                    non_zero_sentences = []
                    syntactic = self.calculate_syntactic(matrix_terms[i], matrix_terms[j], non_zero_sentences, aspect_class_object)
                db.add_syntactic(matrix_terms[i], matrix_terms[j], syntactic)
            print(datetime.now() - start)
            if count % 1000 == 0:
                db.conn_syntactic.commit()

    @staticmethod
    def calculate_syntactic(aspect1, aspect2, non_zero_sentences, aspect_class_object):
        syntactic_path = 0
        for sentence in non_zero_sentences:
            syntactic_tree = Aspects.syntatic_parsing(sentence, aspect_class_object)
            data = json.loads(syntactic_tree)
            items = data['annotations']['syntax-relation']
            # todo
        return syntactic_path
