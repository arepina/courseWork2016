import json

import requests
from aspects.DB import DB
from aspects.PMI import PMI


class Aspects:
    api_key = "43de6ee952010c5e0870b999f2a1949183456c73"
    url_syntatic_parsing = \
        "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="
    url_pos = "http://api.ispras.ru/texterra/v3.1/nlp/pos?filtering=KEEPING&class=pos-token&apikey="
    url_sentence = "http://api.ispras.ru/texterra/v3.1/nlp/sentence?filtering=KEEPING&class=sentence&apikey="
    texts = None

    def __init__(self):
        self.url_syntatic_parsing += self.api_key
        self.url_pos += self.api_key
        self.url_sentence += self.api_key

    def process(self):
        row_aspect = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        count = 0
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_aspect[2])
            adv = str(row_aspect[3])
            dis = str(row_aspect[4])
            com = str(row_aspect[5])
            if len(adv) != 0:
                adv_parsed = self.syntatic_parsing(adv)
                list_adv_aspects = self.aspects_find(adv_parsed)  # load aspects for advantage
            else:
                list_adv_aspects = []

            if len(dis) != 0:
                dis_parsed = self.syntatic_parsing(dis)
                list_dis_aspects = self.aspects_find(dis_parsed)  # load aspects for disadvantage
            else:
                list_dis_aspects = []

            if len(com) != 0:
                com_parsed = self.syntatic_parsing(com)
                list_com_aspects = self.aspects_find(com_parsed)  # load aspects for comment
            else:
                list_com_aspects = []
            # join the results
            str_adv_aspects = ';'.join(list_adv_aspects)
            str_dis_aspects = ';'.join(list_dis_aspects)
            str_com_aspects = ';'.join(list_com_aspects)
            # add found information to DB
            db.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row_aspect = db.cursor_reviews.fetchone()

    @staticmethod
    def syntatic_parsing(review):  # detects syntactic structure for each sentence of a given text
        try:
            payload = {'text': str(review)}
            headers = {'Accept': 'application/json'}
            r = requests.post(aspect.url_syntatic_parsing, data=payload, headers=headers)
            while r.status_code != 200:
                r = requests.post(aspect.url_syntatic_parsing, data=payload, headers=headers)
            return r.content.decode('utf8')
        except Exception:
            import sys
            type, value, traceback = sys.exc_info()  # (<class 'requests.exceptions.ConnectionError'>, ConnectionError(ProtocolError('Connection aborted.', TimeoutError(10060, 'Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже подключенного компьютера', None, 10060, None)),), <traceback object at 0x0667AB48>)
            print('Error opening %s: %s' % (value.filename, value.strerror))
            return None

    def aspects_find(self, part):  # find aspects in each review part
        list_aspects = []  # list with aspects
        print(part)
        data = json.loads(part)
        items = data['annotations']['syntax-relation']
        pos_arr = self.parse_pos(self.tag_part_of_speech(data['text']))
        for item in items:  # iterate through words/word pairs in concrete review
            if 'parent' in item['value']:  # word pair
                # look for aspect noun(parent) + word
                list_aspects = self.word_pair(data, item, list_aspects, pos_arr)
            else:  # one word
                # look for aspect noun(word)
                list_aspects = self.one_word(data, item, list_aspects, pos_arr)
        return list_aspects

    def one_word(self, data, item, list_aspects, pos_arr):
        start = item['start']
        end = item['end']
        word = data['text'][start:end]
        if pos_arr[str(word)] == 'S':  # our word is noun
            list_aspects.append(self.replacer(word))  # add an aspect noun(our word)
        return list_aspects

    def word_pair(self, data, item, list_aspects, pos_arr):
        word = data['text'][item['start']:item['end']]
        parent = data['text'][item['value']['parent']['start']:item['value']['parent']['end']]
        pos_parent = pos_arr[str(parent)]
        pos_word = pos_arr[str(word)]
        if pos_parent == 'S' and pos_word != 'PUNCT' and pos_word != 'CONJ' and pos_word != 'PR':
            # don't need punctuations, conjunctions, pretexts as words
            # find pairs: S(parent) + smf
            start_par = item['value']['parent']['start']
            start_word = item['start']
            if start_par < start_word:  # the word order is important in if-idf calculation
                # add an aspect noun(parent) + our word
                list_aspects.append(self.replacer(parent) + " " + self.replacer(word))
            else:
                # add an aspect noun(parent) + our word
                list_aspects.append(self.replacer(word) + " " + self.replacer(parent))
        elif pos_word == 'S':
            list_aspects.append(self.replacer(word))  # add an aspect noun(our word)
        return list_aspects

    @staticmethod
    def replacer(item):
        item = item.replace(",", "")
        item = item.replace(".", "")
        item = item.replace("•", "")
        item = item.replace(";", "")
        item = item.replace("!", "")
        item = item.replace("?", "")
        item = item.replace(")", "")
        item = item.replace("(", "")
        item = item.replace("™", "")
        item = item.replace("®", "")
        item = item.replace("*", "")
        item = item.replace("\"", "")
        item = item.replace("—", "")
        item = item.replace("~", "")
        item = item.replace("'", "")
        return item.lower()

    @staticmethod
    def parse_pos(pos_sentence):
        sentence = json.loads(pos_sentence)
        pos_items = sentence['annotations']['pos-token']
        result = {}
        for item in pos_items:
            text = sentence['text'][item['start']:item['end']]
            result[text] = item['value']['tag']
        return result

    @staticmethod
    def tag_part_of_speech(item):  # detects part of speech tag for each word of a given text
        payload = {'text': str(item)}
        headers = {'Accept': 'application/json'}
        r = requests.post(aspect.url_pos, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(aspect.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')

    def move_ideal_aspects(self, ideal, ideal_aspects):
        row_aspect = db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
        count = 0
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_aspect[0])
            adv = str(row_aspect[1])
            dis = str(row_aspect[2])
            com = str(row_aspect[3])
            ideal_adv = self.get_ideal(adv, ideal_aspects)
            ideal_dis = self.get_ideal(dis, ideal_aspects)
            ideal_com = self.get_ideal(com, ideal_aspects)
            # join the results
            str_adv_aspects = ';'.join(ideal_adv)
            str_dis_aspects = ';'.join(ideal_dis)
            str_com_aspects = ';'.join(ideal_com)
            ideal.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row_aspect = db.cursor_aspects.fetchone()

    @staticmethod
    def get_ideal(part, ideal_aspects):
        aspect_arr = []
        if len(part) != 0:
            splitted_part = part.split(";")
            for item in splitted_part:
                if item in ideal_aspects:
                    aspect_arr.append(item)
        return aspect_arr


class Splitter:
    def process(self):
        row_review = db.cursor_reviews_one_word.execute('SELECT * FROM Reviews').fetchone()
        count = 0
        while row_review is not None:
            print(count)
            count += 1
            article = str(row_review[0])
            adv_before = str(row_review[1])
            adv = self.clean(adv_before, article)
            adv = " ".join(adv.split())
            if adv_before != adv:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET advantageAspects = ? WHERE advantageAspects = ?',
                    (adv, adv_before, ))
                db.conn_reviews_one_word.commit()
            dis_before = str(row_review[2])
            dis = self.clean(dis_before, article)
            dis = " ".join(dis.split())
            if dis_before != dis:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET disadvantageAspects = ? WHERE disadvantageAspects = ?',
                    (dis, dis_before, ))
                db.conn_reviews_one_word.commit()
            com_before = str(row_review[3])
            com = self.clean(com_before, article)
            com = " ".join(com.split())
            if com_before != com:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET commentAspects = ? WHERE commentAspects = ?',
                    (com, com_before, ))
                db.conn_reviews_one_word.commit()
            row_review = db.cursor_reviews_one_word.fetchone()

    @staticmethod
    def clean(part, article):
        new_part = ""
        words = part.strip().split(" ")
        words = filter(None, words)
        for word in words:
            if word[0] == "_":
                if len(word) == 1:
                    word = ""
                else:
                    word = word[1:]
            if len(word) > 0 and word[len(word) - 1] == "_":
                word = word[0:len(word) - 1]
            if word.isdigit():
                word = ""
            if word.count("_") > 1:
                under_words = word.split("_")
                if len(under_words) == 3:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[2]
                elif len(under_words) == 4:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[2] + " " + under_words[2] + "_" + under_words[3]
                elif len(under_words) == 7:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[2] + " " + under_words[2] + "_" + under_words[3] + " " + under_words[3] + "_" + under_words[4] + " " + under_words[4] + "_" + under_words[5] + " " + under_words[5] + "_" + under_words[6]
                else:
                    new_str = ""
                new_part += new_str + " "
            else:
                new_part += word + " "
        return new_part.strip()


db = DB()  # data base
aspect = Aspects()
sp = Splitter()
sp.process()


pmi = PMI()
vocabulary = pmi.get_vocabulary(db)
reviews_corpus = pmi.get_all_reviews_corpus(db)
sentences_corpus = pmi.get_all_sentences_corpus(db)
db.create_pmi_review_db()
pmi.calculate_pmi(reviews_corpus, True, vocabulary, db)
db.create_pmi_sentence_db()
pmi.calculate_pmi(sentences_corpus, False, vocabulary, db)
# aspect.process()  # find aspects with the help of ISP RAS API
# one_class_svm = OneClassSVM()
# data = one_class_svm.get_data(db)  # get only aspects from data base
# # get labels for all the aspects depends on their ideality
# labels = one_class_svm.get_labels(data, db)
# # split the data (80% for training)
# train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)
# # unarray the 2D arrays and make them 1D
# test_data_unarrayed = one_class_svm.unarray(test_data)
# train_data_unarrayed = one_class_svm.unarray(train_data)
# train_labels_unarrayed = one_class_svm.unarray(train_labels)
# # get only ideal aspects from aspects list (label = 1) for train data
# train_data_unarrayed = one_class_svm.get_ideal_data(train_data_unarrayed, train_labels_unarrayed)
# # train the one-class SVM and predict the aspects
# test_labels_unarrayed = one_class_svm.train_and_predict(train_data_unarrayed, test_data_unarrayed)
# # get only ideal aspects from aspects list (label = 1) for test data
# test_data_unarrayed = one_class_svm.get_ideal_data(test_data_unarrayed, test_labels_unarrayed)
# # now the sum of test_data_unarrayed and train_data_unarrayed have only ideal aspects
# ideal_aspects = test_data_unarrayed + train_data_unarrayed
# ideal.count_aspects()  # number of idel aspects
# # got only ideal aspects in the db
# aspect.move_ideal_aspects(ideal, ideal_aspects)
# synonyms = Synonyms()
# synonyms.find_synonyms(ideal)  # find and group the synonyms
# sentence = Sentence(db)
# sentence.process(db, aspect)  # create a db with all sentences from reviews

# len(data, labels) = 24093
# len(train_data, train_labels) = 19274
# len(test_data, test_labels) = 4819
# len(train_data_unarrayed) = 619286
# len(test_data_unarrayed) = 154951
# len(all_aspects) = 774237
# len(ideal_train_data_unarrayed) = 46149
# len(ideal_test_data_unarrayed) = 124709
# len(ideal_aspects_dictionary) = 170858
# len(ideal_aspects) = 540571
# len(grouped aspects) = 421715
# len(vocabulary) = 45435
