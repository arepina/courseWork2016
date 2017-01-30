import nltk
import numpy as np
from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer


class Context:
    def process(self, db, vocabulary):
        db.create_context_db()
        reviews = self.get_reviews(db)
        # self.form_global_db(db, vocabulary, reviews)
        self.global_context(vocabulary, db)
        self.local_context(vocabulary, db, reviews)

    @staticmethod
    def get_reviews(db):
        reviews = []
        row_review = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        while row_review is not None:
            adv = str(row_review[3])
            dis = str(row_review[4])
            com = str(row_review[5])
            review = adv + " " + dis + " " + com
            reviews.append(review.lower())
            row_review = db.cursor_reviews_one_word.fetchone()
        return reviews

    @staticmethod
    def form_global_db(db, vocabulary, reviews):
        count = 0
        for aspect in vocabulary:
            print(count)
            count += 1
            clear_aspect = aspect.lower().replace("_", " ")
            str_context = ""
            for review in reviews:
                # todo what to do if aspect parts are held in different places of review
                if clear_aspect in review:
                    # try to find every 2 left and 2 right words for aspect
                    words = review.split(' ')
                    aspect_indexes = np.where(np.array(words) == clear_aspect)[0]
                    for index in aspect_indexes:
                        # if there is no 2 left or no 2 right words make their str empty = _
                        if index - 1 < 0:
                            left_1 = "_"
                        else:
                            left_1 = words[index - 1]
                        if index - 2 < 0:
                            left_2 = "_"
                        else:
                            left_2 = words[index - 2]
                        if index + 1 > len(words) - 1:
                            right_1 = "_"
                        else:
                            right_1 = words[index + 1]
                        if index + 2 > len(words) - 1:
                            right_2 = "_"
                        else:
                            right_2 = words[index + 2]
                        if len(str_context) > 0:
                            str_context += " "
                        str_context += left_2 + " " + left_1 + " " + right_1 + " " + right_2
            db.add_context(clear_aspect, str_context)
            db.conn_context.commit()

    def local_context(self, vocabulary, db, reviews):
        # todo calculate the kl-divergence for local context
        pass

    @staticmethod
    def global_context(vocabulary, db):
        # aspect_row = db.cursor_context.execute('SELECT * FROM Context').fetchone()
        # while aspect_row is not None:
        #     aspect = str(aspect_row[0])
        #     context = str(aspect_row[1])
        #     tokenize = nltk.word_tokenize(context)
        #     four_grams = ngrams(tokenize, 4)
        #     vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        #     matrix = vectorizer.fit_transform(four_grams)
        #     matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        #     matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect
        #     # todo calculate the kl-divergence for global context
        #     aspect_row = db.cursor_context.fetchone()
        context = str("a b c d e f g h i g k l")
        tokenize = nltk.word_tokenize(context)
        four_grams = ngrams(tokenize, 4)
        vectorizer = CountVectorizer(min_df=5, max_df=0.8, vocabulary=vocabulary)
        matrix = vectorizer.fit_transform(four_grams)
        matrix_terms = np.array(vectorizer.get_feature_names())  # unique aspects - keys
        matrix_freq = np.asarray(matrix.sum(axis=0)).ravel()  # number of each aspect

    @staticmethod
    def kl_divergence(p, q):
        """ Compute KL divergence of two vectors, K(p || q)."""
        from cmath import log
        return sum(p[x] * log((p[x]) / (q[x])) for x in range(len(p)) if p[x] != 0.0 or p[x] != 0)
