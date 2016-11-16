import json

import requests
import sqlite3


class Aspects:
    conn_aspects = None
    conn_reviews = None
    cursor_aspects = None
    cursor_reviews = None
    cursor_article = None
    cursor_num = None
    db_aspects_name = 'Aspects_Ulmart.db'
    db_reviews_name = 'Review_Ulmart.db'
    api_key = "e68469466a70c5d3b8c8a91c091b12a35d8dd529"
    url_syntatic_parsing = "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="
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
    def add_review(self, article, advantageAspects, disadvantageAspects, commentAspects):
        self.cursor_aspects.execute(
            'INSERT INTO Aspects (article, advantageAspects, disadvantageAspects, commentAspects) '
            'VALUES (?, ?, ?, ?)',
            (article, advantageAspects, disadvantageAspects, commentAspects))
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

    def aspects_find(self):
        self.cursor_reviews.execute('SELECT * FROM Review')
        row = self.cursor_reviews.fetchone()
        while row is not None:
            print(str(row))
            article = str(row[2])
            all_reviews_num = self.cursor_num.execute('SELECT COUNT(*) FROM Review WHERE article = ' + str(article)).fetchone()[0]
            aspects_already_have = self.cursor_article.execute('SELECT COUNT(*) FROM Aspects WHERE article = ' + str(article)).fetchone()[0]
            if aspects_already_have == all_reviews_num:  # we have already downloaded all the aspects for this product
                row = self.cursor_reviews.fetchone()
                continue
            list_adv_aspects = self.api_aspects(self.process(str(row[3])))
            list_dis_aspects = self.api_aspects(self.process(str(row[4])))
            list_com_aspects = self.api_aspects(self.process(str(row[5])))
            str_adv_aspects = ';'.join(list_adv_aspects)
            str_dis_aspects = ';'.join(list_dis_aspects)
            str_com_aspects = ';'.join(list_com_aspects)
            self.add_review(article, str_adv_aspects, str_dis_aspects, str_com_aspects)
            row = self.cursor_reviews.fetchone()

    def process(self, review):
        payload = {'text': str(review)}
        headers = {'Accept': 'application/json'}
        r = requests.post(self.url_syntatic_parsing, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(self.url_syntatic_parsing, data=payload, headers=headers)
        return r.content.decode('utf8')

    def api_aspects(self, part):
        list_aspects = []  # list with aspects
        print(part)
        data = json.loads(part)
        items = data['annotations']['syntax-relation']
        for item in items:  # iterate through words/word pairs in concrete review
            if 'parent' in item['value']:  # word pair
                list_aspects = self.word_pair(data, item, items, list_aspects)
            else:  # one word
                list_aspects = self.one_word(item, data, list_aspects)
        return list_aspects

    def one_word(self, item, data, list_aspects):
        start = item['start']
        end = item['end']
        word_value = data['text'][start:end]
        tag_pos = self.tag_part_of_speech(word_value)
        pos = json.loads(tag_pos)['annotations']['pos-token'][0]['value']['tag']
        if pos == 'S':  # our word is noun
            list_aspects.append(word_value.lower())  # add an aspect noun(our word)
        return list_aspects

    def part_find(self, items, data, parent, parent_value, word_value, list_aspects):
        for extra_item in items:
            if 'parent' in extra_item['value']:
                word_valueExtra = data['text'][extra_item['start']:extra_item['end']]
                parentExtra = extra_item['value']['parent']
                parent_valueExtra = data['text'][parentExtra['start']:parentExtra['end']]
                if parentExtra['start'] == parent['start'] \
                        and parentExtra['end'] == parent['end'] \
                        and parent_value == parent_valueExtra:
                    tag_pos_wordExtra = self.tag_part_of_speech(word_valueExtra)
                    pos_wordExtra = json.loads(tag_pos_wordExtra)['annotations']['pos-token'][0]['value']['tag']
                    if pos_wordExtra == 'PART' and extra_item['value']['type'] != '2-компл':
                        list_aspects.append(word_valueExtra.lower() + " " + parent_value.lower() + " " + word_value.lower())  # add an aspect noun(parent) + our word
                        break
        list_aspects.append(parent_value.lower() + " " + word_value.lower())  # add an aspect noun(parent) + our word
        return list_aspects
    
    def word_pair(self, data, item, items, list_aspects):
        word_value = data['text'][item['start']:item['end']]
        parent = item['value']['parent']
        parent_value = data['text'][parent['start']:parent['end']]
        tag_pos_parent = self.tag_part_of_speech(parent_value)
        tag_pos_word = self.tag_part_of_speech(word_value)
        pos_parent = json.loads(tag_pos_parent)['annotations']['pos-token'][0]['value']['tag']
        pos_word = json.loads(tag_pos_word)['annotations']['pos-token'][0]['value']['tag']
        if (pos_parent == 'S' and pos_word != 'PUNCT' and pos_word != 'CONJ' and pos_word != 'PR') \
                or (pos_word == 'S' and pos_parent != 'PUNCT' and pos_parent != 'CONJ'):
            # don't need punctuations, conjunctions, pretexts
            if pos_parent == 'PR' or pos_parent == 'V':  # try to find PART for PR or PART for V
                list_aspects = self.part_find(items, data, parent, parent_value, word_value, list_aspects)
            else:
                list_aspects.append(parent_value.lower() + " " + word_value.lower())  # add an aspect noun(parent) + our word
        return list_aspects

    def tag_part_of_speech(self, parent):
        payload = {'text': str(parent)}
        headers = {'Accept': 'application/json'}
        r = requests.post(self.url_pos, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(self.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')


aspects = Aspects()
aspects.aspects_find()
