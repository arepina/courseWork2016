import json

import requests


class Sentence:

    def __init__(self, db):
        db.create_sentence_db()

    def process(self, db, aspect):
        row_aspect = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        count = 0
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            if count > 23997:
                article = str(row_aspect[2])
                adv = str(row_aspect[3]).strip()
                review = ""
                if len(adv) != 0:
                    review += adv
                    if adv[len(adv) - 1] != "." and adv[len(adv) - 1] != "!" and adv[len(adv) - 1] != "?":
                        review += "."
                dis = str(row_aspect[4]).strip()
                if len(dis) != 0:
                    if len(review) != 0:
                        review += " "
                    review += dis
                    if dis[len(dis) - 1] != "." and dis[len(dis) - 1] != "!" and dis[len(dis) - 1] != "?":
                        review += "."
                com = str(row_aspect[5]).strip()
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
            row_aspect = db.cursor_reviews.fetchone()

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
