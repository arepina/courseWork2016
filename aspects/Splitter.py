
class Splitter:
    def process_reviews(self, db):
        row_review = db.cursor_reviews_one_word.execute('SELECT * FROM Reviews').fetchone()
        count = 0
        while row_review is not None:
            print(count)
            count += 1
            adv_before = str(row_review[1])
            adv = self.clean(adv_before)
            adv = " ".join(adv.split())
            if adv_before != adv:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET advantageAspects = ? WHERE advantageAspects = ?',
                    (adv, adv_before,))
                db.conn_reviews_one_word.commit()
            dis_before = str(row_review[2])
            dis = self.clean(dis_before)
            dis = " ".join(dis.split())
            if dis_before != dis:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET disadvantageAspects = ? WHERE disadvantageAspects = ?',
                    (dis, dis_before,))
                db.conn_reviews_one_word.commit()
            com_before = str(row_review[3])
            com = self.clean(com_before)
            com = " ".join(com.split())
            if com_before != com:
                db.cursor_reviews_one_word_update.execute(
                    'UPDATE Reviews SET commentAspects = ? WHERE commentAspects = ?',
                    (com, com_before,))
                db.conn_reviews_one_word.commit()
            row_review = db.cursor_reviews_one_word.fetchone()

    def process_sentences(self, db):
        row_sentence = db.cursor_sentences_one_word.execute('SELECT * FROM Sentences').fetchone()
        count = 0
        while row_sentence is not None:
            print(count)
            count += 1
            sentence_before = str(row_sentence[1])
            sentence = self.clean(sentence_before)
            sentence = " ".join(sentence.split())
            if sentence_before != sentence:
                db.cursor_sentences_one_word_update.execute(
                    'UPDATE Sentences SET sentence = ? WHERE sentence = ?',
                    (sentence, sentence_before,))
                db.conn_reviews_one_word.commit()
            row_sentence = db.cursor_sentences_one_word.fetchone()

    @staticmethod
    def clean(part):
        new_part = ""
        words = part.strip().split(" ")
        words = filter(None, words)
        for word in words:
            if word[0] == "_":
                if len(word) == 1:
                    word = ""
                else:
                    word = word[1:]
            if len(word) > 0 and word[len(word) - 1] == "_":
                word = word[0:len(word) - 1]
            if word.isdigit():
                word = ""
            if word.count("_") > 1:
                under_words = word.split("_")
                if len(under_words) == 3:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[2]
                elif len(under_words) == 4:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[
                        2] + " " + under_words[2] + "_" + under_words[3]
                elif len(under_words) == 7:
                    new_str = under_words[0] + "_" + under_words[1] + " " + under_words[1] + "_" + under_words[
                        2] + " " + under_words[2] + "_" + under_words[3] + " " + under_words[3] + "_" + under_words[
                                  4] + " " + under_words[4] + "_" + under_words[5] + " " + under_words[5] + "_" + \
                              under_words[6]
                else:
                    new_str = ""
                new_part += new_str + " "
            else:
                new_part += word + " "
        return new_part.strip()

