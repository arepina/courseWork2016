class Synonyms:

    def find_synonyms(self, ideal):
        row_aspect = ideal.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
        count = 1
        while row_aspect is not None:  # iterate through all reviews
            print(count)
            count += 1
            article = str(row_aspect[0])
            adv = str(row_aspect[1])
            dis = str(row_aspect[2])
            com = str(row_aspect[3])
            tree_adv = self.build_trees(adv)
            tree_dis = self.build_trees(dis)
            tree_com = self.build_trees(com)
            adv_items = ';'.join('{}{}'.format(key, val) for key, val in tree_adv.items())
            dis_items = ';'.join('{}{}'.format(key, val) for key, val in tree_dis.items())
            com_items = ';'.join('{}{}'.format(key, val) for key, val in tree_com.items())
            ideal.add_review(article, adv_items, dis_items, com_items)
            row_aspect = ideal.cursor_aspects.fetchone()

    @staticmethod
    def find_whole_word(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def build_trees(self, part):
        tree = {}
        if len(part) != 0:
            aspects = part.split(";")
            for i in range(len(aspects)):
                if len(aspects[i].split(" ")) == 1:
                    flag = False
                    for item in tree:
                        if self.find_whole_word(aspects[i])(item) and flag == False:
                            flag = True
                            tree.pop(item, None)
                            str_without_item = item.replace(aspects[i], "").strip()
                            tree[aspects[i]] = "{" + str_without_item + "}"
                    for j in range(i + 1, len(aspects)):
                        if self.find_whole_word(aspects[i])(aspects[j]) and len(aspects[j].split(" ")) != 1:
                            flag = True
                            str_without_item = aspects[j].replace(aspects[i], "").strip()
                            if aspects[i] not in tree:
                                tree[aspects[i]] = "{" + str_without_item + "}"
                            else:
                                tree[aspects[i]] = tree[aspects[i]][1:len(tree[aspects[i]]) - 1]
                                tree[aspects[i]] = "{" + tree[aspects[i]] + "," + str_without_item + "}"
                    if not flag:
                        tree[aspects[i]] = ""
                else:
                    words = aspects[i].split(" ")
                    for w in words:
                        flag = False
                        for item in tree:
                            if self.find_whole_word(w)(item):
                                flag = True
                        if not flag:
                            tree[aspects[i]] = ""
                        else:
                            break
        return tree

