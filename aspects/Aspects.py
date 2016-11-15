import json

from lxml import etree

import requests
import sqlite3

from lxml.etree import XML


class Aspects:
    conn_aspects = None
    conn_reviews = None
    cursor_aspects = None
    cursor_reviews = None
    db_aspects_name = 'Aspects_Ulmart.db'
    db_reviews_name = 'Review_Ulmart.db'
    api_key = "e68469466a70c5d3b8c8a91c091b12a35d8dd529"
    url = "http://api.ispras.ru/texterra/v3.1/nlp/syntax?filtering=KEEPING&class=syntax-relation&apikey="

    def __init__(self):
        self.url += self.api_key
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
             (article TEXT, advantageAspects TEXT, disadvantageAspects TEXT, commentAspects Text)''')
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
            advantage_processed = self.process(str(row[3]))
            print(advantage_processed)
            e = etree.fromstring(advantage_processed)
            from xml.etree import cElementTree as ET
            #xml = ET.fromstring(advantage_processed).get('NLP-document')
            data = XML(advantage_processed).find("NLP-document")
            for iannotation in e.findall('I-annotation'):
                print(iannotation)
            disadvantage_processed = self.process(str(row[4]))
            comment_processed = self.process(str(row[5]))


            #self.add_review(str(row[2]), advantage_aspect, disadvantage_aspect, comment_aspect)
            row = self.cursor_reviews.fetchone()

    def process(self, review):
        payload = {'text': str(review)}
        headers = {'Accept': 'application/json'}
        r = requests.post(self.url,data=json.dumps(payload), headers=headers)
        while r.status_code != 200:
            r = requests.post(self.url, data={'text': str(review)})
        print(r.content)
        return 0
        # import pycurl, json
        # c = pycurl.Curl()
        # c.setopt(pycurl.URL, self.url)
        # c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        # data = json.dumps({"text": review})
        # c.setopt(pycurl.POST, 1)
        # c.setopt(pycurl.POSTFIELDS, data)
        # c.setopt(pycurl.VERBOSE, 1)
        # c.perform()
        # #print (curl_agent.getinfo(pycurl.RESPONSE_CODE))
        # c.close()



aspects = Aspects()
aspects.aspects_find()
