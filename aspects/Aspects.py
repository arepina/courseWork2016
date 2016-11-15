import json

import requests
import sqlite3


class Aspects:
    conn_aspects = None
    conn_reviews = None
    cursor_aspects = None
    cursor_reviews = None
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

    def aspects_find(self):
        self.cursor_reviews.execute('SELECT * FROM Review')
        row = self.cursor_reviews.fetchone()
        while row is not None:
            print(str(row))
            self.adv_aspects(row)
            #disadvantage_processed = self.process(str(row[4]))
            #comment_processed = self.process(str(row[5]))

            # self.add_review(str(row[2]), advantage_aspect, disadvantage_aspect, comment_aspect)
            row = self.cursor_reviews.fetchone()

    def adv_aspects(self, row):
        advantage_processed = self.process(str(row[3]))
        print(advantage_processed)
        data = json.loads(advantage_processed)
        items = data['annotations']['syntax-relation']
        for item in items:  # iterate through words in advantage review
            print(item)
            if 'parent' in item['value']:
                parent = item['value']['parent']
                start = parent['start']
                end = parent['end']
                parent_value = data['text'][start:end - start]
                if item['value']['type'] != 'PUNCT':
                    tag_pos = self.tag_part_of_speech(parent_value)
                    print(tag_pos)
                    data_pos = json.loads(tag_pos)
                    pos = data_pos['annotations']['pos-token'][0]['value']['tag']
                    if pos == 'S':  # parent is noun
                        t = 44
                        #todo case if parent is noun
            else:
                t = 44  #todo check case if the word is noun!!!!

    def process(self, review):
        payload = {'text': str(review)}
        headers = {'Accept': 'application/json'}
        r = requests.post(self.url_syntatic_parsing, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(self.url_syntatic_parsing, data=payload, headers=headers)
        return r.content.decode('utf8')

    def tag_part_of_speech(self, parent):
        payload = {'text': str(parent)}
        headers = {'Accept': 'application/json'}
        r = requests.post(self.url_pos, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(self.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')


aspects = Aspects()
aspects.aspects_find()
