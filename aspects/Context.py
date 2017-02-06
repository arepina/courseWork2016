import numpy as np
import sklearn.feature_extraction.text


class Context:
    def process(self, db, vocabulary):  # todo think about vocabulary
        reviews = self.get_reviews(db)  # get user reviews
        db.create_context_local_prepare_db()
        db.create_context_global_prepare_db()
        # fill the db where the aspects with 4-words substrs as context their context are were calculated
        self.form_local_context_db(db, vocabulary, reviews)
        self.local_context(db, vocabulary)  # calculate the local context
        self.form_global_context_db(db, vocabulary, reviews)
        self.global_context(db, vocabulary)  # calculate the global context
        # In both calculations we build language model for each aspect, then we calculate the KL - divergence
        # for every language model combination. The difference between global and local contexts is that in global
        # we take words from all the reviews and in local we consider only the words of concrete review.

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

    def form_local_context_db(self, db, vocabulary, reviews):
        for aspect in vocabulary:
            clear_aspect = aspect.lower().replace("_", " ")
            str_context = ""
            for review in reviews:
                clear_aspect_words = clear_aspect.split(" ")
                if len(clear_aspect_words) == 1:  # the aspect is only 1 word
                    str_context = self.is_one_word_aspect_in_review(clear_aspect, review, str_context, False)
                else:  # the aspect consists of several words
                    str_context = self.is_several_word_aspect_in_review(clear_aspect_words, review, str_context, False)
            db.add_context_local_prepare(aspect, str_context)  # collect the 4 words context for each aspect occurrence
            db.conn_local_context_prepare.commit()

    def form_global_context_db(self, db, vocabulary, reviews):
        for aspect in vocabulary:
            clear_aspect = aspect.lower().replace("_", " ")
            str_context = ""
            for review in reviews:
                clear_aspect_words = clear_aspect.split(" ")
                if len(clear_aspect_words) == 1:  # the aspect is only 1 word
                    is_aspect_in_review = self.is_one_word_aspect_in_review(clear_aspect, review, str_context, True)
                else:  # the aspect consists of several words
                    is_aspect_in_review = self.is_several_word_aspect_in_review(clear_aspect_words, review, str_context,
                                                                                True)
                if is_aspect_in_review:  # collect all the reviews with the aspect
                    db.add_context_global_prepare(aspect, review)
            db.conn_global_context_prepare.commit()

    def is_several_word_aspect_in_review(self, clear_aspect_words, review, str_context, is_global):
        is_all_aspect_words_in_review = True
        for word in clear_aspect_words:
            if word not in review:
                is_all_aspect_words_in_review = False
                break
        if is_global:
            return is_all_aspect_words_in_review
        if is_all_aspect_words_in_review:
            # if aspect parts are held in different places of review take the left and the right word
            left_aspect_part = clear_aspect_words[0]
            right_aspect_part = clear_aspect_words[len(clear_aspect_words) - 1]
            words = review.split(' ')
            left_aspect_part_index = np.where(np.array(words) == left_aspect_part)[0][0]
            right_aspect_part_index = np.where(np.array(words) == right_aspect_part)[0][0]
            left = self.check_left_index(left_aspect_part_index, words)
            right = self.check_right_index(right_aspect_part_index, words)
            if len(str_context) > 0:
                str_context += " "
            str_context += left + " " + right
        return str_context

    def is_one_word_aspect_in_review(self, aspect, review, str_context, is_global):
        if aspect in review:
            # try to find every 2 left and 2 right words for aspect
            words = review.split(' ')
            aspect_indexes = np.where(np.array(words) == aspect)[0]
            # find 2 left and 2 right word for each aspect occurrence
            for index in aspect_indexes:
                str_context = self.form_str_context(index, words, str_context)
        if is_global:
            if len(str_context) > 0:
                return True
            else:
                return False
        return str_context

    def form_str_context(self, index, words, str_context):
        # if there is no 2 left or no 2 right words make their str as _BEGIN_SENTENCE_ and _END_SENTENCE_
        left = self.check_left_index(index, words)
        right = self.check_right_index(index, words)
        if len(str_context) > 0:
            str_context += " "
        str_context += left + " " + right
        return str_context

    @staticmethod
    def check_left_index(index, words):
        if index - 1 < 0:
            left_1 = "_BEGIN_SENTENCE_"
        else:
            left_1 = words[index - 1]
        if index - 2 < 0:
            left_2 = "_BEGIN_SENTENCE_"
        else:
            left_2 = words[index - 2]
        return left_2 + " " + left_1

    @staticmethod
    def check_right_index(index, words):
        if index + 1 > len(words) - 1:
            right_1 = "_END_SENTENCE_"
        else:
            right_1 = words[index + 1]
        if index + 2 > len(words) - 1:
            right_2 = "_END_SENTENCE_"
        else:
            right_2 = words[index + 2]
        return right_1 + " " + right_2

    def local_context(self, db, vocabulary):
        count = 0
        context_for_aspects_dict = {}
        db.create_context_local_db()
        vectorizer = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(1, 1),
                                                                     vocabulary=vocabulary)
        aspect_row = db.cursor_local_context_prepare.execute('SELECT * FROM Context').fetchone()
        # load all the data from context db to context_for_aspects_dict
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            context_for_aspects_dict[count] = [aspect, context]
            aspect_row = db.cursor_local_context_prepare.fetchone()
            count += 1
        # look through all aspect pairs to calculate their kl_divergence
        for i in range(len(context_for_aspects_dict)):
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect1 = context_for_aspects_dict[i][0]
                aspect2 = context_for_aspects_dict[j][0]
                # the strs with many 4-words substrs which were calculated in form_context_db method for each aspect
                aspect1_context = context_for_aspects_dict[i][1]
                aspect2_context = context_for_aspects_dict[j][1]
                ngram1 = vectorizer.fit_transform(aspect1_context)  # get ngram
                ngram2 = vectorizer.fit_transform(aspect2_context)  # get ngram
                # calculate the kl-divergence for local context
                kl_diver = self.kl_divergence(ngram1.toarray(),
                                              ngram2.toarray())  # send 2 unigram language models in vector form
                db.add_context_local(aspect1, aspect2, kl_diver)
            db.conn_local_context.commit()

    def global_context(self, db, vocabulary):
        count = 0
        context_for_aspects_dict = {}
        db.create_context_global_db()
        vectorizer = sklearn.feature_extraction.text.CountVectorizer(ngram_range=(1, 1), vocabulary=vocabulary)
        # load all the data from context db to context_for_aspects_dict
        for aspect in vocabulary:
            aspect_row = db.cursor_global_context_prepare.execute('SELECT * FROM Context WHERE aspect = ?', (aspect,)).fetchone()
            context = ""
            while aspect_row is not None:
                context += str(aspect_row[1]) + " "
                aspect_row = db.cursor_global_context_prepare.fetchone()
            context_for_aspects_dict[count] = [aspect, context]
            count += 1
        # look through all aspect pairs to calculate their kl_divergence
        for i in range(len(context_for_aspects_dict)):
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect1 = context_for_aspects_dict[i][0]
                aspect2 = context_for_aspects_dict[j][0]
                # the strs with many 4-words substrs which were calculated in form_context_db method for each aspect
                aspect1_context = context_for_aspects_dict[i][1]
                aspect2_context = context_for_aspects_dict[j][1]
                ngram1 = vectorizer.fit_transform(aspect1_context)  # get ngram
                ngram2 = vectorizer.fit_transform(aspect2_context)  # get ngram
                # calculate the kl-divergence for global context
                kl_diver = self.kl_divergence(ngram1.toarray(),
                                              ngram2.toarray())  # send 2 unigram language models in vector form
                db.add_context_global(aspect1, aspect2, kl_diver)
            db.conn_global_context.commit()

    @staticmethod
    def kl_divergence(p, q):
        """ Compute KL divergence of two vectors, K(p || q)."""
        from cmath import log
        return sum(p[x] * log((p[x]) / (q[x])) for x in range(len(p)) if p[x] != 0.0 or p[x] != 0)
