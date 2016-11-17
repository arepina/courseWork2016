import json

import requests
import sqlite3


class AspectsDB:
    conn_aspects = None
    conn_reviews = None
    cursor_aspects = None
    cursor_reviews = None
    cursor_article = None
    cursor_num = None
    db_aspects_name = 'Aspects_Ulmart.db'
    db_reviews_name = 'Review_Ulmart.db'
    api_key = "e68469466a70c5d3b8c8a91c091b12a35d8dd529"
    url_syntatic_parsing = \
        "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="
    url_pos = "http://api.ispras.ru/texterra/v3.1/nlp/pos?filtering=KEEPING&class=pos-token&apikey="

    def __init__(self):
        self.url_syntatic_parsing += self.api_key
        self.url_pos += self.api_key
        import os
        path = os.getcwd()
        self.conn_aspects = sqlite3.connect(path + "\\..\\db\\" + self.db_aspects_name)
        self.conn_reviews = sqlite3.connect(path + "\\..\\db\\" + self.db_reviews_name)
        self.cursor_aspects = self.conn_aspects.cursor()
        self.cursor_reviews = self.conn_reviews.cursor()
        self.cursor_article = self.conn_aspects.cursor()
        self.cursor_num = self.conn_reviews.cursor()
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

    def aspects_find(self):
        aspect_db.cursor_reviews.execute('SELECT * FROM Review')
        row = aspect_db.cursor_reviews.fetchone()
        while row is not None:  # iterate through all reviews
            print(str(row))
            article = str(row[2])
            all_reviews_num = \
                aspect_db.cursor_num.execute('SELECT COUNT(*) FROM Review WHERE article = ' + str(article)).fetchone()[
                    0]  # number of reviews with concrete article
            aspects_already_have = \
                aspect_db.cursor_article.execute('SELECT COUNT(*) FROM Aspects WHERE article = ' + str(article)).fetchone()[
                    0]  # number of reviews with concrete article we have already processed
            if aspects_already_have == all_reviews_num:  # we have already downloaded all the aspects for this product
                row = aspect_db.cursor_reviews.fetchone()
                continue
            list_adv_aspects = self.aspects(self.syntatic_parsing(str(row[3])))  # load aspects for advantage
            list_dis_aspects = self.aspects(self.syntatic_parsing(str(row[4])))  # load aspects for disadvantage
            list_com_aspects = self.aspects(self.syntatic_parsing(str(row[5])))  # load aspects for comment
            str_adv_aspects = ';'.join(list_adv_aspects)
            str_dis_aspects = ';'.join(list_dis_aspects)
            str_com_aspects = ';'.join(list_com_aspects)
            # add found information to DB
            aspect_db.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row = aspect_db.cursor_reviews.fetchone()

    @staticmethod
    def syntatic_parsing(review):  # detects syntactic structure for each sentence of a given text
        payload = {'text': str(review)}
        headers = {'Accept': 'application/json'}
        r = requests.post(aspect_db.url_syntatic_parsing, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(aspect_db.url_syntatic_parsing, data=payload, headers=headers)
        return r.content.decode('utf8')

    def aspects(self, part):  # find aspects in each review part
        list_aspects = []  # list with aspects
        print(part)
        data = json.loads(part)
        items = data['annotations']['syntax-relation']
        for item in items:  # iterate through words/word pairs in concrete review
            if 'parent' in item['value']:  # word pair
                list_aspects = self.word_pair(data, item, items, list_aspects)  # look for aspect noun(parent) + word
            else:  # one word
                found = False
                for aspect_item in list_aspects:
                    if data['text'][item['start']:item['end']] in aspect_item:  # we have already found a better variant for these word
                        found = True
                        break
                if not found:
                    list_aspects = self.one_word(item, data, list_aspects)  # look for aspect noun(word)
        return list_aspects

    def one_word(self, item, data, list_aspects):
        start = item['start']
        end = item['end']
        word = data['text'][start:end]
        tag_pos = self.tag_part_of_speech(word)  # detects part of speech tag for each word of a given text
        pos = json.loads(tag_pos)['annotations']['pos-token'][0]['value']['tag']
        if pos == 'S':  # our word is noun
            list_aspects.append(word.lower())  # add an aspect noun(our word)
        return list_aspects

    def part_find(self, items, data, parent, parent_value, word, list_aspects):
        for item in items:  # look through all words in review part
            if 'parent' in item['value']:
                word_valueExtra = data['text'][item['start']:item['end']]
                parent_valueExtra = data['text'][item['value']['parent']['start']:item['value']['parent']['end']]
                if item['value']['parent']['start'] == parent['start'] \
                        and item['value']['parent']['end'] == parent['end'] \
                        and parent_value == parent_valueExtra:  # the found word and word from parameters are the same
                    tag_pos_wordExtra = self.tag_part_of_speech(
                        word_valueExtra)  # detects part of speech tag for each word of a given text
                    pos_wordExtra = json.loads(tag_pos_wordExtra)['annotations']['pos-token'][0]['value']['tag']
                    if pos_wordExtra == 'PART' and item['value']['type'] != '2-компл':
                        list_aspects.append(
                            word_valueExtra.lower() + " " + parent_value.lower() + " " + word.lower())  # add an aspect part + noun(parent) + our word
                        return list_aspects
        list_aspects.append(parent_value.lower() + " " + word.lower())  # add an aspect noun(parent) + our word
        return list_aspects

    def word_pair(self, data, item, items, list_aspects):
        word = data['text'][item['start']:item['end']]
        parent = data['text'][item['value']['parent']['start']:item['value']['parent']['end']]
        tag_pos_parent = self.tag_part_of_speech(parent)  # detects part of speech tag for each word of a given text
        tag_pos_word = self.tag_part_of_speech(word)  # detects part of speech tag for each word of a given text
        pos_parent = json.loads(tag_pos_parent)['annotations']['pos-token'][0]['value']['tag']
        pos_word = json.loads(tag_pos_word)['annotations']['pos-token'][0]['value']['tag']
        if (pos_parent == 'S' and pos_word != 'PUNCT' and pos_word != 'CONJ' and pos_word != 'PR') \
                or (pos_word == 'S' and pos_parent != 'PUNCT' and pos_parent != 'CONJ'):
            # don't need punctuations, conjunctions, pretexts as main words
            # find pairs: S(parent) + smf or S(word) + smf
            if pos_parent == 'PR' or pos_parent == 'V':  # try to find PART for PR or for V (не для *, не доделал *)
                list_aspects = self.part_find(items, data, item['value']['parent'], parent, word, list_aspects)
            else:
                list_aspects.append(parent.lower() + " " + word.lower())  # add an aspect noun(parent) + our word
        return list_aspects

    def tag_part_of_speech(self, parent):  # detects part of speech tag for each word of a given text
        payload = {'text': str(parent)}
        headers = {'Accept': 'application/json'}
        r = requests.post(aspect_db.url_pos, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(aspect_db.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')

    def tf_idf(self, word, review_part):
        td_idf_value = self.tf(word, review_part) * self.idf(word)
        return td_idf_value

    def tf(self, word, review_part):
        counter = 0
        words_review = review_part.split()
        words_num = len(words_review)
        for item in words_review:
            item = self.replacer(item)  # remove punctuation
            if word == item:
                counter += 1
        return counter / words_num

    def idf(self, word):
        counter = 0
        all_reviews_num = 24093
        aspect_db.cursor_num.execute('SELECT * FROM Review')
        row = aspect_db.cursor_num.fetchone()
        while row is not None:  # iterate through all reviews
            adv = str(row[3])  # advantage
            dis = str(row[4])  # disadvantage
            com = str(row[5])  # comment
            if word in adv or word in dis or word in com:
                counter += 1
            row = aspect_db.cursor_num.fetchone()
        import math
        return math.log10(all_reviews_num / counter)

    def replacer(self, item):
        item = item.replace(",", "")
        item = item.replace(".", "")
        item = item.replace(";", "")
        item = item.replace("!", "")
        item = item.replace("?", "")
        return item


aspect_db = AspectsDB()
aspect = Aspects()
aspect.aspects_find()
