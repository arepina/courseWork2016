from datetime import datetime

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


class PMI:
    @staticmethod
    def get_all_ideal_aspects_from_train_files():
        import os
        ideal_aspects_from_file = {}
        path = os.getcwd()
        filenames = os.listdir(path + "\\..\\productTrees\\Subcategories")
        os.chdir(path + "\\..\\productTrees\\Subcategories")
        count = 0
        for filename in filenames:
            with open(filename) as f:
                lines = f.readlines()
            arr = lines[0].split(";")
            for val in arr:
                val = val.replace(" ", "_").lower()
                val = val.replace(",_", "_")
                if val not in ideal_aspects_from_file:
                    ideal_aspects_from_file[val] = count
                    count += 1
        return ideal_aspects_from_file

    @staticmethod
    def get_all_reviews_corpus(db):
        reviews = []
        row_review = db.cursor_reviews_one_word.execute('SELECT * FROM Reviews').fetchone()
        while row_review is not None:
            adv = str(row_review[1])
            dis = str(row_review[2])
            com = str(row_review[3])
            review = adv + " " + dis + " " + com
            reviews.append(review)
            row_review = db.cursor_reviews_one_word.fetchone()
        return reviews

    @staticmethod
    def get_all_sentences_corpus(db):
        sentences = []
        row_sentence = db.cursor_sentences_one_word.execute('SELECT * FROM Sentences').fetchone()
        while row_sentence is not None:
            sentence = str(row_sentence[1])
            sentences.append(sentence)
            row_sentence = db.cursor_sentences_one_word.fetchone()
        return sentences

    @staticmethod
    def get_vocabulary(db):
        vocabulary = {}
        row = db.cursor_aspects_one_word.execute('SELECT * FROM Aspects').fetchone()
        count = 0
        while row is not None:
            adv = str(row[1]).strip()
            if len(adv) != 0:
                items = adv.split(";")
                for item in items:
                    if item not in vocabulary and len(item) > 0:
                        vocabulary[item] = count
                        count += 1
            dis = str(row[2]).strip()
            if len(dis) != 0:
                items = dis.split(";")
                for item in items:
                    if item not in vocabulary and len(item) > 0:
                        vocabulary[item] = count
                        count += 1
            com = str(row[3]).strip()
            if len(com) != 0:
                items = com.split(";")
                for item in items:
                    if item not in vocabulary and len(item) > 0:
                        vocabulary[item] = count
                        count += 1
            row = db.cursor_aspects_one_word.fetchone()
        return vocabulary

    def one_word_aspects(self, ideal, db):
        row_aspect = ideal.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
        count = 0
        while row_aspect is not None:
            print(count)
            count += 1
            article = str(row_aspect[0])
            adv = str(row_aspect[1])
            list_adv_aspects = self.create_one_word_list(adv)
            dis = str(row_aspect[2])
            list_dis_aspects = self.create_one_word_list(dis)
            com = str(row_aspect[3])
            list_com_aspects = self.create_one_word_list(com)
            str_adv_aspects = ';'.join(list_adv_aspects)
            str_dis_aspects = ';'.join(list_dis_aspects)
            str_com_aspects = ';'.join(list_com_aspects)
            db.add_one_word_aspects(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row_aspect = ideal.cursor_aspects.fetchone()
        db.conn_aspects_one_word.commit()

    def one_word_reviews(self, db):
        row = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        row_aspect = db.cursor_aspects_one_word.execute('SELECT * FROM Aspects').fetchone()
        count = 0
        while row is not None:
            print(count)
            count += 1
            article = str(row[2])
            adv = str(row[3]).lower()
            adv_aspect = str(row_aspect[1])
            adv = self.process_review(adv, adv_aspect)
            dis = str(row[4]).lower()
            dis_aspect = str(row_aspect[2])
            dis = self.process_review(dis, dis_aspect)
            com = str(row[5]).lower()
            com_aspect = str(row_aspect[3])
            com = self.process_review(com, com_aspect)
            db.add_one_word_review(article, adv, dis, com)
            row = db.cursor_reviews.fetchone()
            row_aspect = db.cursor_aspects_one_word.fetchone()
        db.conn_reviews_one_word.commit()

    @staticmethod
    def process_review(part, aspects):
        if len(aspects) != 0:
            items = aspects.split(";")
            for item in items:
                old_words = item.split("_")
                if len(old_words) > 1:
                    for word in old_words:
                        part = part.replace(word, "", 1)  # remove the 1st entry of aspect word
                else:
                    part = part.replace(old_words[0], "", 1)
                if len(part) == 0 or part[len(part) - 1] == " " or part[len(part) - 1] == "_":
                    part += item
                else:
                    part += " " + item
        return part

    @staticmethod
    def create_one_word_list(part):
        if len(part) != 0:
            arr = []
            items = part.split(";")
            for item in items:
                words = item.split(" ")
                if len(words) > 1:
                    arr.append("_".join(words))
                else:
                    arr.append(words[0])
            return arr
        return ""

    def calculate_pmi_review(self, corpus, which_part, vocabulary, db):
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        count = 0
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect
        final_matrix = np.array([matrix_terms, matrix_freq])
        col_array = self.create_col_array(matrix, len(matrix_terms))
        col_array = np.array(col_array)
        from math import log
        for i in range(len(matrix_terms)):
            print(count)
            count += 1
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                col1 = col_array[i]
                col2 = col_array[j]
                both_num = np.count_nonzero(col1 * col2)
                if both_num == 0:  # independent
                    pmi_val = 0
                else:
                    pmi_val = log(both_num / (int(final_matrix[1][i]) * int(final_matrix[1][j])))
                if which_part == 0:
                    db.add_pmi_review(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                      both_num, pmi_val)
                elif which_part == 1:
                    db.add_pmi_sentence(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                        both_num, pmi_val)
                elif which_part == 2:
                    db.add_pmi_ideal_review(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                            both_num, pmi_val)
                else:
                    db.add_pmi_ideal_sentence(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                              both_num, pmi_val)
            print(datetime.now() - start)
            if count % 1000 == 0:
                db.conn_pmi_sentence.commit()

    def calculate_pmi_sentence(self, corpus, vocabulary, db):
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        count = 0
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect
        final_matrix = np.array([matrix_terms, matrix_freq])
        col_array = self.create_col_array(matrix, len(matrix_terms))
        col_array1 = np.array(col_array[:5000])
        col_array2 = np.array(col_array[5000:10000])
        col_array3 = np.array(col_array[10000:15000])
        col_array4 = np.array(col_array[15000:20000])
        col_array5 = np.array(col_array[20000:25000])
        col_array6 = np.array(col_array[25000:30000])
        col_array7 = np.array(col_array[30000:35000])
        col_array8 = np.array(col_array[35000:40000])
        col_array9 = np.array(col_array[40000:])
        from math import log
        for i in range(len(matrix_terms)):
            print(count)
            count += 1
            start = datetime.now()
            for j in range(i + 1, len(matrix_terms)):
                if i < 5000:
                    col1 = col_array1[i]
                elif i < 10000:
                    col1 = col_array2[i - 5000]
                elif i < 15000:
                    col1 = col_array3[i - 10000]
                elif i < 20000:
                    col1 = col_array4[i - 15000]
                elif i < 25000:
                    col1 = col_array5[i - 20000]
                elif i < 30000:
                    col1 = col_array6[i - 25000]
                elif i < 35000:
                    col1 = col_array7[i - 30000]
                elif i < 40000:
                    col1 = col_array8[i - 35000]
                else:
                    col1 = col_array9[i - 40000]
                if j < 5000:
                    col2 = col_array1[j]
                elif j < 10000:
                    col2 = col_array2[j - 5000]
                elif j < 15000:
                    col2 = col_array3[j - 10000]
                elif j < 20000:
                    col2 = col_array4[j - 15000]
                elif j < 25000:
                    col2 = col_array5[j - 20000]
                elif j < 30000:
                    col2 = col_array6[j - 25000]
                elif j < 35000:
                    col2 = col_array7[j - 30000]
                elif j < 40000:
                    col2 = col_array8[j - 35000]
                else:
                    col2 = col_array9[j - 40000]
                both_num = np.count_nonzero(col1 * col2)
                if both_num == 0:  # independent
                    pmi_val = 0
                else:
                    pmi_val = log(both_num / (int(final_matrix[1][i]) * int(final_matrix[1][j])))
                db.add_pmi_sentence(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                    both_num, pmi_val)
            print(datetime.now() - start)
            if count % 1000 == 0:
                db.conn_pmi_sentence.commit()

    @staticmethod
    def create_col_array(matrix, matrix_terms_len):
        array = []
        from nltk.compat import xrange
        for i in xrange(matrix_terms_len):
            col = np.array(matrix[:, i].T.toarray())
            array.append(col)
        return array
