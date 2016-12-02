import json
import os

import sys

# from nltk.text import TextCollection
import requests

from sklearn.model_selection import train_test_split

from aspects.AspectsDB import AspectsDB
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

from aspects.IdealAspectsDB import IdealAspectsDB


class Aspects:
    api_key = "43de6ee952010c5e0870b999f2a1949183456c73"
    url_syntatic_parsing = \
        "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="
    url_pos = "http://api.ispras.ru/texterra/v3.1/nlp/pos?filtering=KEEPING&class=pos-token&apikey="
    texts = None

    def __init__(self):
        self.url_syntatic_parsing += self.api_key
        self.url_pos += self.api_key
        # row = aspect_db.cursor_merged.execute('SELECT * FROM Reviews').fetchone()
        # texts_arr = []
        # while row is not None:  # iterate through all reviews
        #     texts_arr.append(str(row[0]).lower())
        #     row = aspect_db.cursor_merged.fetchone()
        # self.texts = TextCollection(texts_arr)  # add all values to text collection

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
            type, value, traceback = sys.exc_info()  # (<class 'requests.exceptions.ConnectionError'>, ConnectionError(ProtocolError('Connection aborted.', TimeoutError(10060, 'Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже подключенного компьютера', None, 10060, None)),), <traceback object at 0x0667AB48>)
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
                list_aspects = self.word_pair(data, item, items, list_aspects,
                                              pos_arr)  # look for aspect noun(parent) + word
            else:  # one word
                found = False
                for aspect_item in list_aspects:
                    if data['text'][item['start']:item[
                        'end']] in aspect_item:  # we have already found a better variant for these word
                        found = True
                        break
                if not found:
                    list_aspects = self.one_word(item, data, list_aspects, pos_arr)  # look for aspect noun(word)
        return list_aspects

    @staticmethod
    def one_word(item, data, list_aspects, pos_arr):
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
                    list_aspects = self.part_find(items, data, item['value']['parent'], parent, word, list_aspects,
                                                  pos_arr, start_par, start_word)
                else:
                    if start_par < start_word:  # the word order is important in if-idf calculation
                        list_aspects.append(
                            parent.lower() + " " + word.lower())  # add an aspect noun(parent) + our word
                    else:
                        list_aspects.append(
                            word.lower() + " " + parent.lower())  # add an aspect noun(parent) + our word
        except:
            pass
        return list_aspects

    @staticmethod
    def part_find(items, data, parent, parent_value, word, list_aspects, pos_arr, start_par, start_word):
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
                        if start_word < start_par and start_word < start_extra_word:  # the word order is important in if-idf calculation
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
        row_aspect = aspect_db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
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
            row_aspect = aspect_db.cursor_aspects.fetchone()

    @staticmethod
    def get_ideal(part, ideal_aspects):
        aspect_arr = []
        if len(part) != 0:
            splitted_part = part.split(";")
            for item in splitted_part:
                index = item.index("{")
                if item[0:index] in ideal_aspects:
                    aspect_arr.append(item[0:index])
        return aspect_arr


class OneClassSVM:

    @staticmethod
    def get_data():
        row = aspect_db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
        data = []
        while row is not None:  # iterate through all reviews
            aspect_arr = []
            if len(str(row[1])) != 0:
                adv = str(row[1]).split(";")
                for item in adv:
                    index = item.index("{")
                    aspect_arr.append(item[0:index])
            if len(str(row[2])) != 0:
                dis = str(row[2]).split(";")
                for item in dis:
                    index = item.index("{")
                    aspect_arr.append(item[0:index])
            if len(str(row[3])) != 0:
                com = str(row[3]).split(";")
                for item in com:
                    index = item.index("{")
                    aspect_arr.append(item[0:index])
            data.append(aspect_arr)
            row = aspect_db.cursor_aspects.fetchone()
        return data

    @staticmethod
    def get_labels(data):
        row_review = aspect_db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        path = os.getcwd()
        train_labels = []
        count = 0
        while row_review is not None:
            subcat_name = str(row_review[1])
            file_path = path + "\\..\\productTrees\\Subcategories\\" + subcat_name + ".txt"
            ideal_labels = []
            labels = []
            with open(file_path) as f:
                ideal_labels.append(f.readlines())
            ideal_labels[0][0] = ideal_labels[0][0].lower()
            for item in data[count]:
                if item in ideal_labels[0][0]:
                    labels.append(1)
                else:
                    labels.append(-1)
            count += 1
            train_labels.append(labels)
            row_review = aspect_db.cursor_reviews.fetchone()
        return train_labels

    @staticmethod
    def get_ideal_data(data, labels):
        ideal_data = []
        for i in range(len(labels)):
            if labels[i] == 1:
                ideal_data.append(data[i])
        return ideal_data

    @staticmethod
    def unarray(data):
        unarrayed_data = []
        for i in range(len(data)):
            for item in data[i]:
                unarrayed_data.append(item)
        return unarrayed_data

    @staticmethod
    def train_and_predict(train_data, test_data):
        vectorizer = TfidfVectorizer(min_df=5,
                                     max_df=0.8,
                                     sublinear_tf=True,
                                     use_idf=True)
        train_vectors = vectorizer.fit_transform(train_data)
        test_vectors = vectorizer.transform(test_data)
        classifier_rbf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
        classifier_rbf.fit(train_vectors)
        prediction_rbf = classifier_rbf.predict(test_vectors)
        return prediction_rbf


class Synonyms:

    def find_synoyms(self, ideal):
        path = os.getcwd() + "\\..\\aspects\\synmaster.txt"
        dictionary = []
        with open(path) as f:
            dictionary.append(f.readlines())
        row_aspect = ideal.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
        count = 0
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_aspect[0])
            adv = str(row_aspect[1])
            dis = str(row_aspect[2])
            com = str(row_aspect[3])
            ideal_adv = self.remove_synonyms(adv, dictionary)
            ideal_dis = self.remove_synonyms(dis, dictionary)
            ideal_com = self.remove_synonyms(com, dictionary)
            # join the results
            str_adv_aspects = ';'.join(ideal_adv)
            str_dis_aspects = ';'.join(ideal_dis)
            str_com_aspects = ';'.join(ideal_com)
            ideal.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row_aspect = aspect_db.cursor_aspects.fetchone()

    @staticmethod
    def remove_synonyms(part, dictionary):
        part_with_no_synonyms = []
        if len(part) != 0:
            aspects = part.split(";")
            for i in range(len(aspects)):
                dict_str = dictionary[aspects[i]]
                j = i + 1
                for j in range(len(aspects)):
                    # todo check if there are any equal aspects
                    r = 42
        return part_with_no_synonyms


aspect_db = AspectsDB()  # aspects data base
aspect = Aspects()  # find aspects with the help of ISP RAS API
one_class_svm = OneClassSVM()
data = one_class_svm.get_data()  # get only aspects from data base
# get labels for all the aspects depends on their ideality
labels = one_class_svm.get_labels(data)
# split the data (80% for training)
test_data, train_data, test_labels, train_labels = train_test_split(data, labels, test_size=0.2)
# unarray the 2D arrays and make them 1D
test_data_unarrayed = one_class_svm.unarray(test_data)
train_data_unarrayed = one_class_svm.unarray(train_data)
train_labels_unarrayed = one_class_svm.unarray(train_labels)
# get only ideal aspects from aspects list (label = 1) for train data
train_data_unarrayed = one_class_svm.get_ideal_data(train_data_unarrayed, train_labels_unarrayed)
# train the one-class SVM and predict the aspects
test_labels_unarrayed = one_class_svm.train_and_predict(train_data_unarrayed, test_data_unarrayed)
# get only ideal aspects from aspects list (label = 1) for test data
test_data_unarrayed = one_class_svm.get_ideal_data(test_data_unarrayed, test_labels_unarrayed)
# now the sum of test_data_unarrayed and train_data_unarrayed have only ideal aspects
ideal_aspects = test_data_unarrayed + train_data_unarrayed
ideal = IdealAspectsDB()
# got only ideal aspects in the db
aspect.move_ideal_aspects(ideal, ideal_aspects)
synonyms = Synonyms()

