import nltk
from nltk import ngrams

from aspects.PMI import PMI


class Context:
    def process(self, db, vocabulary):
        db.create_context_local_db()
        db.create_context_global_db()
        reviews = PMI.get_all_reviews_corpus(db)
        self.global_context(vocabulary, db, reviews)
        self.local_context(vocabulary, db, reviews)

    def local_context(self, vocabulary, db, reviews):
        # todo calculate the kl-divergence for local context
        pass

    @staticmethod
    def global_context(vocabulary, db, reviews):
        for aspect in vocabulary:
            str_context = ""
            for review in reviews:
                if aspect in review:
                    # try to find every 2 left and 2 right words for aspect
                    words = review.split(' ')
                    import numpy as np
                    aspect_indexes = np.where(np.array(words) == aspect)[0]
                    for index in aspect_indexes:
                        # todo what to do if there is no 2 left or no 2 right words?
                        left_1 = words[index - 1]
                        left_2 = words[index - 2]
                        right_1 = words[index + 1]
                        right_2 = words[index + 2]
                        str_context += left_2 + left_1 + right_1 + right_2
            db.add_context(aspect, str_context)
            db.conn_context.commit()
        aspect_row = db.cursor_context.execute('SELECT * FROM Context').fetchone()
        while aspect_row is not None:
            aspect = str(aspect_row[0])
            context = str(aspect_row[1])
            tokenize = nltk.word_tokenize(context)
            four_grams = ngrams(tokenize, 4)
            # todo calculate the kl-divergence for global context
            aspect_row = db.cursor_context.fetchone()

    @staticmethod
    def kl_divergence(p, q):
        """ Compute KL divergence of two vectors, K(p || q)."""
        from cmath import log
        return sum(p[x] * log((p[x]) / (q[x])) for x in range(len(p)) if p[x] != 0.0 or p[x] != 0)
