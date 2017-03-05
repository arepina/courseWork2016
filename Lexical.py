

class Lexical:

    @staticmethod
    def process(aspects, db):
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

    @staticmethod
    def process_ideal(db):
        db.create_lexical_ideal_db()
        row_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        while row_ideal is not None:
            aspect1 = str(row_ideal[0])
            aspect2 = str(row_ideal[1])
            length_difference = abs(len(aspect1) - len(aspect2))
            db.add_lexical_ideal(aspect1, aspect2, length_difference)
            row_ideal = db.cursor_pmi_ideal_review.fetchone()
        db.conn_lexical_ideal.commit()

