import json

import sys
from nltk.text import TextCollection
import requests
import sqlite3
import os

from sklearn.feature_extraction.text import TfidfVectorizer


class AspectsDB:
    conn_aspects = None
    conn_reviews = None
    conn_merged = None

    cursor_aspects = None
    cursor_reviews = None
    cursor_article = None
    cursor_merged = None

    db_merged_name = 'Merged.db'
    db_aspects_name = 'Aspects_Ulmart.db'
    db_reviews_name = 'Review_Ulmart.db'

    def __init__(self):
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_reviews = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_name)
        self.conn_merged = sqlite3.connect(path + "\\..\\db\\" + self.db_merged_name)

        self.cursor_merged = self.conn_merged.cursor()
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_reviews = self.conn_reviews.cursor()
        self.cursor_article = self.conn_aspects.cursor()

        self.create_aspects_db()

    # Create table
    def create_aspects_db(self):
        self.cursor_aspects.execute('''CREATE TABLE IF NOT EXISTS Aspects
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects TEXT)''')
        self.commit()

    # Insert new review to DB
    def add_review(self, article, advantage_aspects, disadvantage_aspects, comment_aspects):
        self.cursor_aspects.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantage_aspects, disadvantage_aspects, comment_aspects))
        self.commit()

    # destructor - close connection
    def __del__(self):
        self.conn_aspects.close()
        self.conn_reviews.close()

    # commit
    def commit(self):
        self.conn_aspects.commit()

    def delete_aspects(self, article):
        self.cursor_aspects.execute('DELETE FROM Aspects WHERE article = ' + str(article))
        self.commit()


class Aspects:
    api_key = "43de6ee952010c5e0870b999f2a1949183456c73"
    url_syntatic_parsing = \
        "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="
    url_pos = "http://api.ispras.ru/texterra/v3.1/nlp/pos?filtering=KEEPING&class=pos-token&apikey="
    texts = None

    def __init__(self):
        self.url_syntatic_parsing += self.api_key
        self.url_pos += self.api_key
        row = aspect_db.cursor_merged.execute('SELECT * FROM Reviews').fetchone()
        texts_arr = []
        while row is not None:  # iterate through all reviews
            texts_arr.append(str(row[0]).lower())
            row = aspect_db.cursor_merged.fetchone()
        self.texts = TextCollection(texts_arr)  # add all values to text collection

    def aspects_find(self):
        row_aspect = aspect_db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        count = 0
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            if count > 3063:
                article = str(row_aspect[2])
                adv = str(row_aspect[3])
                dis = str(row_aspect[4])
                com = str(row_aspect[5])
                if len(adv) != 0:
                    adv_parsed = self.syntatic_parsing(adv)
                    while adv_parsed is None:
                        adv_parsed = self.syntatic_parsing(adv)
                    list_adv_aspects = self.aspects(adv_parsed)  # load aspects for advantage
                else:
                    list_adv_aspects = []

                if len(dis) != 0:
                    dis_parsed = self.syntatic_parsing(dis)
                    while dis_parsed is None:
                        dis_parsed = self.syntatic_parsing(dis)
                    list_dis_aspects = self.aspects(dis_parsed)  # load aspects for disadvantage
                else:
                    list_dis_aspects = []

                if len(com) != 0:
                    com_parsed = self.syntatic_parsing(com)
                    while com_parsed is None:
                        com_parsed = self.syntatic_parsing(com)
                    list_com_aspects = self.aspects(com_parsed)  # load aspects for comment
                else:
                    list_com_aspects = []

                # calculate td-idf value for each aspect
                tdidf_adv = self.td_idf_calculate(list_adv_aspects, adv)
                tdidf_dis = self.td_idf_calculate(list_dis_aspects, dis)
                tdidf_com = self.td_idf_calculate(list_com_aspects, com)
                # join the results
                str_adv_aspects = ';'.join(tdidf_adv)
                str_dis_aspects = ';'.join(tdidf_dis)
                str_com_aspects = ';'.join(tdidf_com)
                # add found information to DB
                aspect_db.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row_aspect = aspect_db.cursor_reviews.fetchone()

    def td_idf_calculate(self, aspects_list, review_part):
        result = []
        for aspect_item in aspects_list:
            value = self.texts.tf_idf(aspect_item.lower(), review_part.lower())
            result.append(aspect_item + "{" + str(value) + "}")
        return result

    def syntatic_parsing(self, review):  # detects syntactic structure for each sentence of a given text
        try:
            payload = {'text': str(review)}
            headers = {'Accept': 'application/json'}
            r = requests.post(aspect.url_syntatic_parsing, data=payload, headers=headers)
            while r.status_code != 200:
                r = requests.post(aspect.url_syntatic_parsing, data=payload, headers=headers)
            return r.content.decode('utf8')
        except Exception:
            type, value, traceback = sys.exc_info() #(<class 'requests.exceptions.ConnectionError'>, ConnectionError(ProtocolError('Connection aborted.', TimeoutError(10060, 'Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже подключенного компьютера', None, 10060, None)),), <traceback object at 0x0667AB48>)
            print('Error opening %s: %s' % (value.filename, value.strerror))
            return None

    def aspects(self, part):  # find aspects in each review part
        list_aspects = []  # list with aspects
        print(part)
        data = json.loads(part)
        items = data['annotations']['syntax-relation']
        pos_arr = self.parse_pos(self.tag_part_of_speech(data['text']))
        for item in items:  # iterate through words/word pairs in concrete review
            if 'parent' in item['value']:  # word pair
                list_aspects = self.word_pair(data, item, items, list_aspects, pos_arr)  # look for aspect noun(parent) + word
            else:  # one word
                found = False
                for aspect_item in list_aspects:
                    if data['text'][item['start']:item['end']] in aspect_item:  # we have already found a better variant for these word
                        found = True
                        break
                if not found:
                    list_aspects = self.one_word(item, data, list_aspects, pos_arr)  # look for aspect noun(word)
        return list_aspects

    def one_word(self, item, data, list_aspects, pos_arr):
        start = item['start']
        end = item['end']
        word = data['text'][start:end]
        if pos_arr[str(word)] == 'S':  # our word is noun
            list_aspects.append(word.lower())  # add an aspect noun(our word)
        return list_aspects

    def word_pair(self, data, item, items, list_aspects, pos_arr):
        try:
            word = data['text'][item['start']:item['end']]
            parent = data['text'][item['value']['parent']['start']:item['value']['parent']['end']]
            pos_parent = pos_arr[str(parent)]
            pos_word = pos_arr[str(word)]
            if (pos_parent == 'S' and pos_word != 'PUNCT' and pos_word != 'CONJ' and pos_word != 'PR') \
                    or (pos_word == 'S' and pos_parent != 'PUNCT' and pos_parent != 'CONJ'):
                # don't need punctuations, conjunctions, pretexts as main words
                # find pairs: S(parent) + smf or S(word) + smf
                start_par = item['value']['parent']['start']
                start_word = item['start']
                if pos_parent == 'PR' or pos_parent == 'V':  # try to find PART for PR or for V (не для *, не доделал *)
                    list_aspects = self.part_find(items, data, item['value']['parent'], parent, word, list_aspects, pos_arr, start_par, start_word)
                else:
                    if start_par < start_word: # the word order is important in if-idf calculation
                        list_aspects.append(parent.lower() + " " + word.lower())  # add an aspect noun(parent) + our word
                    else:
                        list_aspects.append(word.lower() + " " + parent.lower())  # add an aspect noun(parent) + our word
        except:
            pass
        return list_aspects

    def part_find(self, items, data, parent, parent_value, word, list_aspects, pos_arr, start_par, start_word):
        for item in items:  # look through all words in review part
            if 'parent' in item['value']:
                word_value_extra = data['text'][item['start']:item['end']]
                parent_value_extra = data['text'][item['value']['parent']['start']:item['value']['parent']['end']]
                if item['value']['parent']['start'] == parent['start'] \
                        and item['value']['parent']['end'] == parent['end'] \
                        and parent_value == parent_value_extra:  # the found word and word from parameters are the same
                    pos_word_extra = pos_arr[str(word_value_extra)]
                    if pos_word_extra == 'PART' and item['value']['type'] != '2-компл':
                        start_extra_word = item['start']
                        sum = ""
                        if start_word < start_par and start_word < start_extra_word: # the word order is important in if-idf calculation
                            if start_extra_word < start_par:
                                sum += word.lower() + " " + word_value_extra.lower() + " " + parent_value.lower()  # wep
                            else:
                                sum += word.lower() + " " + parent_value.lower() + " " + word_value_extra.lower()  # wpe
                        elif start_par < start_extra_word and start_par < start_word:
                            if start_word < start_extra_word:
                                sum += parent_value.lower() + " " + word.lower() + " " + word_value_extra.lower()  # pwe
                            else:
                                sum += parent_value.lower() + " " + word_value_extra.lower() + " " + word.lower()  # pew
                        elif start_extra_word < start_word and start_extra_word < start_par:
                            if start_par < start_word:
                                sum += word_value_extra.lower() + " " + parent_value.lower() + " " + word.lower()  # epw
                            else:
                                sum += word_value_extra.lower() + " " + word.lower() + " " + parent_value.lower()  # ewp
                        list_aspects.append(sum)  # add an aspect part + noun(parent) + our word
                        return list_aspects
        if start_par < start_word:  # the word order is important in if-idf calculation
            list_aspects.append(parent_value.lower() + " " + word.lower())  # add an aspect noun(parent) + our word
        else:
            list_aspects.append(word.lower() + " " + parent_value.lower())  # add an aspect noun(parent) + our word
        return list_aspects

    def parse_pos(self, pos_sentence):
        sentence = json.loads(pos_sentence)
        pos_items = sentence['annotations']['pos-token']
        result = {}
        for item in pos_items:
            text = sentence['text'][item['start']:item['end']]
            result[text] = item['value']['tag']
        return result

    def tag_part_of_speech(self, item):  # detects part of speech tag for each word of a given text
        payload = {'text': str(item)}
        headers = {'Accept': 'application/json'}
        r = requests.post(aspect.url_pos, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(aspect.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')


class OneClassSVM:

    def get_train_data(self):
        row = aspect_db.cursor_merged.execute('SELECT * FROM Reviews').fetchone()
        train_data = []
        while row is not None:  # iterate through all reviews
            train_data.append(str(row[0]).lower())
            row = aspect_db.cursor_merged.fetchone()
        return train_data

    def get_test_data(self):
        row = aspect_db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
        test_data = []
        while row is not None:  # iterate through all reviews
            aspect_arr = []
            adv = str(row[1]).split(";")
            for item in adv:
                index = item.index("{")
                aspect_arr.append(item[0:index])
            dis = str(row[2]).split(";")
            for item in dis:
                index = item.index("{")
                aspect_arr.append(item[0:index])
            com = str(row[3]).split(";")
            for item in com:
                index = item.index("{")
                aspect_arr.append(item[0:index])
            test_data.append(aspect_arr)
            row = aspect_db.cursor_merged.fetchone()
        return test_data

    def get_train_labels(self):
        import glob
        file_names = glob.glob("/productTres/Subcategories/*.txt")
        train_labels = []
        for name in file_names:
            with open(name) as f:
                train_labels.append(f.readlines())
        return train_labels

    def process(self, train_data, test_data, train_labels):
        vectorizer = TfidfVectorizer(min_df=5,
                             max_df = 0.8,
                             sublinear_tf=True,
                             use_idf=True)
        train_vectors = vectorizer.fit_transform(train_data)
        test_vectors = vectorizer.transform(test_data)

        from sklearn import svm
        classifier_rbf = svm.SVC()
        classifier_rbf.fit(train_vectors, train_labels)
        prediction_rbf = classifier_rbf.predict(test_vectors)


aspect_db = AspectsDB()
aspect = Aspects()
oneclasssvm = OneClassSVM()
train_labels = oneclasssvm.get_train_labels()
train_data = oneclasssvm.get_train_data()
test_data = oneclasssvm.get_test_data()
oneclasssvm.process(train_data, test_data, train_labels)

