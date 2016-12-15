import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


class PMI:
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

    @staticmethod
    def calculate_pmi(corpus, is_review, vocabulary, db):
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(corpus)
        count = 0
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect
        final_matrix = np.array([matrix_terms, matrix_freq])
        for i in range(len(matrix_terms)):
            print(count)
            count += 1
            in_count = 0
            for j in range(i + 1, len(matrix_terms)):
                print("\t" + str(in_count))
                in_count += 1
                col1 = np.array(np.array(matrix[:, i].T.toarray()))
                col2 = np.array(np.array(matrix[:, j].T.toarray()))
                both_num = np.count_nonzero(col1 * col2)
                if both_num == 0:  # independent
                    pmi_val = 0
                else:
                    from math import log
                    pmi_val = log(both_num / (int(final_matrix[1][i]) * int(final_matrix[1][j])))
                if is_review:
                    db.add_pmi_review(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                      both_num, pmi_val)
                else:
                    db.add_pmi_sentence(matrix_terms[i], matrix_terms[j], final_matrix[1][i], final_matrix[1][j],
                                        both_num, pmi_val)
