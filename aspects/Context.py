import codecs
from datetime import datetime
from scipy import stats
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


class Context:
    def process(self, db, aspects):
        all_aspects_words = {}
        reviews = self.get_reviews_and_vocabulary(db, all_aspects_words)  # get user reviews
        db.create_context_local_prepare_db()
        db.create_context_global_prepare_db()
        # fill the db where the aspects with 4-words substrs as context their context are were calculated
        self.form_local_context_db(db, aspects, reviews, 0)
        self.form_global_context_db(db, aspects, reviews, 0)
        self.form_global_context_extra_db(db, aspects)
        print("started")
        self.local_context(db, all_aspects_words)  # calculate the local context
        print("local finished")
        self.global_context(db, all_aspects_words)  # calculate the global context
        print("global finished")
        # In both calculations we build language model for each aspect, then we calculate the KL - divergence
        # for every language model combination. The difference between global and local contexts is that in global
        # we take words from all the reviews and in local we consider only the words of concrete review

    def process_ideal(self, db):
        aspects = self.get_ideal_dict()
        all_aspects_words = {}
        reviews = self.get_reviews_and_vocabulary(db, all_aspects_words)  # get user reviews
        db.create_context_local_prepare_ideal_db()
        db.create_context_global_prepare_ideal_db()
        # fill the db where the aspects with 4-words substrs as context their context are were calculated
        self.form_local_context_db(db, aspects, reviews, 1)
        self.form_global_context_db(db, aspects, reviews, 1)
        self.form_global_context_extra_ideal_db(db, aspects)
        print("started")
        self.local_context_ideal(db, all_aspects_words)  # calculate the local context
        print("local finished")
        self.global_context_ideal(db, all_aspects_words)  # calculate the global context
        print("global finished")
        # In both calculations we build language model for each aspect, then we calculate the KL - divergence
        # for every language model combination. The difference between global and local contexts is that in global
        # we take words from all the reviews and in local we consider only the words of concrete review

    def get_ideal_dict(self):
        import os
        dict = {}
        path = os.getcwd()
        filenames = os.listdir(path + "/../productTrees/Subcategories")
        os.chdir(path + "/../productTrees/Subcategories")
        filenames.remove(".DS_Store")
        filenames.remove("Subcategories.txt")
        count = 0
        for filename in filenames:
            line = codecs.open(filename, 'r', 'cp1251').readlines()[0]
            words = line.split(";")
            for word in words:
                low_word = word.lower().replace(",", " ").replace("  ", " ").replace(" ", "_")
                # клавиатуры!!!! мыши и клавиатуры
                if low_word not in dict:
                    dict[low_word] = count
                    count += 1
        return dict

    def get_reviews_and_vocabulary(self, db, all_aspects_words):
        reviews = []
        row_review = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        count = 0
        while row_review is not None:
            adv = str(row_review[3])
            dis = str(row_review[4])
            com = str(row_review[5])
            review = adv + " " + dis + " " + com
            review = self.replacer(review)
            review = " ".join(review.split())
            reviews.append(review)
            words = review.split(" ")
            for word in words:
                if word not in all_aspects_words:
                    all_aspects_words[word] = count
                    count += 1
            row_review = db.cursor_reviews.fetchone()
        return reviews

    def form_local_context_db(self, db, aspects, reviews, which_part):
        count = 0
        for aspect in aspects:
            print(count)
            clear_aspect = aspect.lower().replace("_", " ")
            str_context = ""
            for review in reviews:
                clear_aspect_words = clear_aspect.split(" ")
                if len(clear_aspect_words) == 1:  # the aspect is only 1 word
                    str_context = self.is_one_word_aspect_in_review(clear_aspect, review, str_context, False)
                else:  # the aspect consists of several words
                    str_context = self.is_several_word_aspect_in_review(clear_aspect_words, review, str_context, False)
            if which_part == 0:
                db.add_context_local_prepare(aspect, str_context)  # collect the 4 words context for each aspect occurrence
                db.conn_local_context_prepare.commit()
            else:  # ideal aspects
                db.add_context_local_prepare_ideal(aspect, str_context)  # collect the 4 words context for each aspect occurrence
                db.conn_local_context_prepare_ideal.commit()
            count += 1

    def form_global_context_db(self, db, aspects, reviews, which_part):
        count = 0
        for aspect in aspects:
            print(count)
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
                    if which_part == 0:
                        db.add_context_global_prepare(aspect, review)
                    else:
                        db.add_context_global_prepare_ideal(aspect, review)
            if which_part == 0:
                db.conn_global_context_prepare.commit()
            else:
                db.conn_global_context_prepare_ideal.commit()
            count += 1

    @staticmethod
    def form_global_context_extra_db(db, aspects):
        db.create_context_global_prepare_extra_db()
        count = 0
        for aspect in aspects:
            print(count)
            aspect_row = db.cursor_global_context_prepare.execute('SELECT * FROM Context WHERE aspect = ?',
                                                                  (aspect,)).fetchone()
            context = ""
            while aspect_row is not None:
                context += str(aspect_row[1]) + " "
                aspect_row = db.cursor_global_context_prepare.fetchone()
            db.add_context_global_prepare_extra(aspect, context)
            db.conn_global_context_prepare_extra.commit()
            count += 1

    @staticmethod
    def form_global_context_extra_ideal_db(db, aspects):
        db.create_context_global_prepare_extra_ideal_db()
        count = 0
        for aspect in aspects:
            print(count)
            aspect_row = db.cursor_global_context_prepare_ideal.execute('SELECT * FROM Context WHERE aspect = ?',
                                                                  (aspect,)).fetchone()
            context = ""
            while aspect_row is not None:
                context += str(aspect_row[1]) + " "
                aspect_row = db.cursor_global_context_prepare_ideal.fetchone()
            db.add_context_global_prepare_extra_ideal(aspect, context)
            db.conn_global_context_prepare_extra_ideal.commit()
            count += 1

    def is_several_word_aspect_in_review(self, clear_aspect_words, review, str_context, is_global):
        is_all_aspect_words_in_review = True
        for word in clear_aspect_words:
            if word not in review.split():
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
        if aspect in review.split():
            if is_global:
                return True
            # try to find every 2 left and 2 right words for aspect
            words = review.split(' ')
            aspect_indexes = np.where(np.array(words) == aspect)[0]
            # find 2 left and 2 right word for each aspect occurrence
            for index in aspect_indexes:
                str_context = self.form_str_context(index, words, str_context)
        if is_global:
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

    def check_left_index(self, index, words):
        if index - 1 < 0:
            left_1 = "_BEGIN_SENTENCE_"
        else:
            left_1 = self.replacer(words[index - 1])
        if index - 2 < 0:
            left_2 = "_BEGIN_SENTENCE_"
        else:
            left_2 = self.replacer(words[index - 2])
        return left_2 + " " + left_1

    def check_right_index(self, index, words):
        if index + 1 > len(words) - 1:
            right_1 = "_END_SENTENCE_"
        else:
            right_1 = self.replacer(words[index + 1])
        if index + 2 > len(words) - 1:
            right_2 = "_END_SENTENCE_"
        else:
            right_2 = self.replacer(words[index + 2])
        return right_1 + " " + right_2

    @staticmethod
    def replacer(item):
        item = item.replace("\r", " ")
        item = item.replace("\t", " ")
        item = item.replace(",", "")
        item = item.replace(".", "")
        item = item.replace("•", "")
        item = item.replace(";", "")
        item = item.replace(":", "")
        item = item.replace("!", "")
        item = item.replace("?", "")
        # item = item.replace(")", "")
        # item = item.replace("(", "")
        item = item.replace("™", "")
        item = item.replace("®", "")
        item = item.replace("*", "")
        item = item.replace("\"", "")
        # item = item.replace("—", "")
        # item = item.replace("-", "")
        item = item.replace("~", "")
        item = item.replace("'", "")
        return item.lower()

    def local_context(self, db, all_aspects_words):
        context_for_aspects_dict = {}
        db.create_context_local_db()
        vectorizer = CountVectorizer(ngram_range=(1, 1), vocabulary=all_aspects_words)
        aspect_row = db.cursor_local_context_prepare.execute('SELECT * FROM Context').fetchone()
        # load all the data from context db to context_for_aspects_dict
        count = 0
        ngram_prepared_dict = {}
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            context_for_aspects_dict[count] = np.array([aspect, context])
            ngram = self.add_one_smoothing(vectorizer.fit_transform([context]).toarray()[0])  # get ngram
            divider = len(context.split())
            if divider != 0:
                ngram = [x / divider for x in ngram]
            ngram_prepared_dict[aspect] = ngram
            aspect_row = db.cursor_local_context_prepare.fetchone()
            count += 1
        print("local rows loaded")
        # look through all aspect pairs to calculate their kl_divergence
        # the strs with many 4-words substrs which were calculated in form_context_db method for each aspect
        for i in range(len(context_for_aspects_dict)):
            print(i)
            start = datetime.now()
            aspect1 = context_for_aspects_dict[i][0]
            ngram1 = ngram_prepared_dict[aspect1]
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect2 = context_for_aspects_dict[j][0]
                ngram2 = ngram_prepared_dict[aspect2]
                # calculate the kl-divergence for local context
                kl_diver = stats.entropy(np.array(ngram1), np.array(ngram2), 2)  # send 2 unigram language models in vector form
                db.add_context_local(aspect1, aspect2, kl_diver)
            db.conn_local_context.commit()
            print(datetime.now() - start)

    def local_context_ideal(self, db, all_aspects_words):
        context_for_aspects_dict = {}
        db.create_context_local_ideal_db()
        vectorizer = CountVectorizer(ngram_range=(1, 1), vocabulary=all_aspects_words)
        aspect_row = db.cursor_local_context_prepare_ideal.execute('SELECT * FROM Context').fetchone()
        # load all the data from context db to context_for_aspects_dict
        count = 0
        ngram_prepared_dict = {}
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            context_for_aspects_dict[count] = np.array([aspect, context])
            ngram = self.add_one_smoothing(vectorizer.fit_transform([context]).toarray()[0])  # get ngram
            divider = len(context.split())
            if divider != 0:
                ngram = [x / divider for x in ngram]
            ngram_prepared_dict[aspect] = ngram
            aspect_row = db.cursor_local_context_prepare_ideal.fetchone()
            count += 1
        print("local rows loaded")
        # look through all aspect pairs to calculate their kl_divergence
        # the strs with many 4-words substrs which were calculated in form_context_db method for each aspect
        for i in range(len(context_for_aspects_dict)):
            print(i)
            start = datetime.now()
            aspect1 = context_for_aspects_dict[i][0]
            ngram1 = ngram_prepared_dict[aspect1]
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect2 = context_for_aspects_dict[j][0]
                ngram2 = ngram_prepared_dict[aspect2]
                # calculate the kl-divergence for local context
                kl_diver = stats.entropy(np.array(ngram1), np.array(ngram2),
                                         2)  # send 2 unigram language models in vector form
                db.add_context_local_ideal(aspect1, aspect2, kl_diver)
            db.conn_local_context_ideal.commit()
            print(datetime.now() - start)

    def global_context(self, db, all_aspects_words):
        count = 0
        context_for_aspects_dict = {}
        db.create_context_global_db()
        vectorizer = CountVectorizer(ngram_range=(1, 1), vocabulary=all_aspects_words)
        # load all the data from context db
        aspect_row = db.cursor_global_context_prepare_extra.execute('SELECT * FROM Context').fetchone()
        ngram_prepared_dict = {}
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            context_for_aspects_dict[count] = [aspect, context]
            ngram = self.add_one_smoothing(vectorizer.fit_transform([context]).toarray()[0])  # get ngram
            divider = len(context.split())
            if divider != 0:
                ngram = [x / divider for x in ngram]
            ngram_prepared_dict[aspect] = ngram
            aspect_row = db.cursor_global_context_prepare_extra.fetchone()
            count += 1
        print("global rows loaded")
        # look through all aspect pairs to calculate their kl_divergence
        for i in range(len(context_for_aspects_dict)):
            print(i)
            start = datetime.now()
            aspect1 = context_for_aspects_dict[i][0]
            ngram1 = ngram_prepared_dict[aspect1]
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect2 = context_for_aspects_dict[j][0]
                ngram2 = ngram_prepared_dict[aspect2]
                # calculate the kl-divergence for global context
                kl_diver = stats.entropy(np.array(ngram1), np.array(ngram2), 2)  # send 2 unigram language models in vector form
                db.add_context_global(aspect1, aspect2, kl_diver)
            db.conn_global_context.commit()
            print(datetime.now() - start)

    def global_context_ideal(self, db, all_aspects_words):
        count = 0
        context_for_aspects_dict = {}
        db.create_context_global_ideal_db()
        vectorizer = CountVectorizer(ngram_range=(1, 1), vocabulary=all_aspects_words)
        # load all the data from context db
        aspect_row = db.cursor_global_context_prepare_extra_ideal.execute('SELECT * FROM Context').fetchone()
        ngram_prepared_dict = {}
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            context_for_aspects_dict[count] = [aspect, context]
            ngram = self.add_one_smoothing(vectorizer.fit_transform([context]).toarray()[0])  # get ngram
            divider = len(context.split())
            if divider != 0:
                ngram = [x / divider for x in ngram]
            ngram_prepared_dict[aspect] = ngram
            aspect_row = db.cursor_global_context_prepare_extra_ideal.fetchone()
            count += 1
        print("global rows loaded")
        # look through all aspect pairs to calculate their kl_divergence
        for i in range(len(context_for_aspects_dict)):
            print(i)
            start = datetime.now()
            aspect1 = context_for_aspects_dict[i][0]
            ngram1 = ngram_prepared_dict[aspect1]
            for j in range(i + 1, len(context_for_aspects_dict)):
                aspect2 = context_for_aspects_dict[j][0]
                ngram2 = ngram_prepared_dict[aspect2]
                # calculate the kl-divergence for global context
                kl_diver = stats.entropy(np.array(ngram1), np.array(ngram2), 2)  # send 2 unigram language models in vector form
                db.add_context_global_ideal(aspect1, aspect2, kl_diver)
            db.conn_global_context_ideal.commit()
            print(datetime.now() - start)

    @staticmethod
    def add_one_smoothing(list):
        for i in range(len(list)):
            if list[i] == 0:
                list[i] = 1
            else:
                list[i] += 1
        return list


