

class Lexical:

    def process(self, aspects, db):
        db.create_lexical_db()
        only_aspect_words = []
        for aspect in aspects:
            only_aspect_words.append(aspect)
        for i in range(len(only_aspect_words)):
            print(i)
            for j in range(i + 1, len(only_aspect_words)):
                length_difference = abs(len(only_aspect_words[i]) - len(only_aspect_words[j]))
                db.add_lexical(only_aspect_words[i], only_aspect_words[j], length_difference)
            db.conn_lexical.commit()

