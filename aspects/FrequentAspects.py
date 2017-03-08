class FrequentAspects:

    def process(self, db):
        db.create_frequent_db()
        row_aspect = db.cursor_aspects_one_word.execute('SELECT * FROM Aspects').fetchone()
        count = 0
        dict = {}
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            adv = str(row_aspect[1])
            dis = str(row_aspect[2])
            com = str(row_aspect[3])
            if len(adv) != 0:
                words = adv.split(";")
                for word in words:
                    if word not in dict:
                        dict[word] = 1
                    else:
                        dict[word] += 1
            if len(dis) != 0:
                words = dis.split(";")
                for word in words:
                    if word not in dict:
                        dict[word] = 1
                    else:
                        dict[word] += 1
            if len(com) != 0:
                words = com.split(";")
                for word in words:
                    if word not in dict:
                        dict[word] = 1
                    else:
                        dict[word] += 1
            row_aspect = db.cursor_aspects_one_word.fetchone()
        # have a dictionary with aspects and their numbers
        import operator
        sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        count = 0
        for word in sorted_dict:
            if count < 1000:
                added_word = self.replacer(word[0])
                db.add_frequent(added_word, word[1])
            else:
                break
            count += 1
        db.conn_frequent.commit()

    @staticmethod
    def replacer(item):
        item = item.replace("\r", " ")
        item = item.replace("\t", " ")
        item = item.replace(",", "")
        item = item.replace(".", "")
        item = item.replace("•", "")
        item = item.replace(";", "")
        item = item.replace(":", "")
        item = item.replace("!", "")
        item = item.replace("?", "")
        item = item.replace(")", "")
        item = item.replace("(", "")
        item = item.replace("™", "")
        item = item.replace("®", "")
        item = item.replace("*", "")
        item = item.replace("\"", "")
        item = item.replace("—", "")
        item = item.replace("-", "")
        item = item.replace("~", "")
        item = item.replace("'", "")
        return item.lower()


