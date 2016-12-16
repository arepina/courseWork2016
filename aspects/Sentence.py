import json

import requests
import re


class Sentence:
    def process(self, db, aspect):
        row_review = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        count = 0
        while row_review is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_review[2])
            adv = str(row_review[3]).strip()
            review = ""
            if len(adv) != 0:
                review += adv
                if adv[len(adv) - 1] != "." and adv[len(adv) - 1] != "!" and adv[len(adv) - 1] != "?":
                    review += "."
            dis = str(row_review[4]).strip()
            if len(dis) != 0:
                if len(review) != 0:
                    review += " "
                review += dis
                if dis[len(dis) - 1] != "." and dis[len(dis) - 1] != "!" and dis[len(dis) - 1] != "?":
                    review += "."
            com = str(row_review[5]).strip()
            if len(com) != 0:
                if len(review) != 0:
                    review += " "
                review += com
                if com[len(com) - 1] != "." and com[len(com) - 1] != "!" and com[len(com) - 1] != "?":
                    review += "."
            sentences_from_api = self.ask_api(review.lower(), aspect)
            sentences = self.clean_sentences(sentences_from_api)
            for sentence in sentences:
                if sentence != ".":
                    db.add_sentence(article, sentence)
            row_review = db.cursor_reviews.fetchone()
        db.conn_sentence.commit()

    def process_one_word(self, db, aspect):
        row_review = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        row_aspect = db.cursor_aspects_one_word.execute('SELECT * FROM Aspects').fetchone()
        count = 0
        while row_review is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_review[2])
            review = ""
            adv = str(row_review[3]).strip()
            adv_aspect = str(row_aspect[1])
            if len(adv) != 0:
                if adv[len(adv) - 1] == "." or adv[len(adv) - 1] == "!" or adv[len(adv) - 1] == "?":
                    adv = adv[0:len(adv) - 1]
            adv = self.process_review(adv, adv_aspect)
            if len(adv) != 0:
                if len(review) != 0:
                    review += " "
                review += adv
                if adv[len(adv) - 1] != "." and adv[len(adv) - 1] != "!" and adv[len(adv) - 1] != "?":
                    review += "."
            dis = str(row_review[4]).strip()
            dis_aspect = str(row_aspect[2])
            if len(dis) != 0:
                if dis[len(dis) - 1] == "." or dis[len(dis) - 1] == "!" or dis[len(dis) - 1] == "?":
                    dis = dis[0:len(dis) - 1]
            dis = self.process_review(dis, dis_aspect)
            if len(dis) != 0:
                if len(review) != 0:
                    review += " "
                review += dis
                if dis[len(dis) - 1] != "." and dis[len(dis) - 1] != "!" and dis[len(dis) - 1] != "?":
                    review += "."
            com = str(row_review[5]).strip()
            com_aspect = str(row_aspect[3])
            if len(com) != 0:
                if com[len(com) - 1] == "." or com[len(com) - 1] == "!" or com[len(com) - 1] == "?":
                    com = com[0:len(com) - 1]
            com = self.process_review(com, com_aspect)
            if len(com) != 0:
                if len(review) != 0:
                    review += " "
                review += com
                if com[len(com) - 1] != "." and com[len(com) - 1] != "!" and com[len(com) - 1] != "?":
                    review += "."
            review = review.upper()
            review = re.sub(' +', ' ', review)
            sentences_from_api = self.ask_api(review, aspect)
            sentences = self.clean_sentences(sentences_from_api)
            for sentence in sentences:
                if sentence != ".":
                    db.add_one_word_sentence(article, sentence.lower())
            row_review = db.cursor_reviews.fetchone()
            row_aspect = db.cursor_aspects_one_word.fetchone()
        db.conn_sentences_one_word.commit()

    @staticmethod
    def process_review(part, aspects):
        if len(aspects) != 0:
            items = aspects.split(";")
            for item in items:
                old_words = item.split("_")
                if len(old_words) > 1:
                    for word in old_words:
                        rep = re.compile(re.escape(word), re.IGNORECASE)
                        part = rep.sub("", part, 1)  # remove the 1st entry of aspect word
                else:
                    rep = re.compile(re.escape(old_words[0]), re.IGNORECASE)
                    part = rep.sub("", part, 1)
                if len(part) == 0 or part[len(part) - 1] == " " or part[len(part) - 1] == "_":
                    part += item
                else:
                    part += " " + item
        return part

    @staticmethod
    def clean_sentences(sentences_from_api):
        result = json.loads(sentences_from_api)
        sentence_items = result['annotations']['sentence']
        sentences = []
        for item in sentence_items:
            text = result['text'][item['start']:item['end']]
            sentences.append(text)
        return sentences

    @staticmethod
    def ask_api(review, aspect):
        payload = {'text': str(review)}
        headers = {'Accept': 'application/json'}
        r = requests.post(aspect.url_sentence, data=payload, headers=headers)
        while r.status_code != 200:
            r = requests.post(aspect.url_pos, data=payload, headers=headers)
        return r.content.decode('utf8')
