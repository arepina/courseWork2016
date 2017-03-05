
class HierarchyBuilder:

    def calculate_average_semantic_distance_ideal_tree(self, db):
        row_review_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence_ideal = db.cursor_pmi_ideal_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical_ideal = db.cursor_lexical_ideal.execute('SELECT * FROM Lexical').fetchone()
        while row_review_ideal is not None:
            pmi_r = float(row_review_ideal[5])
            pmi_s = float(row_sentence_ideal[5])
            lexical = int(row_lexical_ideal[2])

            row_review_ideal = db.cursor_pmi_ideal_review.fetchone()
            row_sentence_ideal = db.cursor_pmi_ideal_sentence.fetchone()
            row_lexical_ideal = db.cursor_lexical_ideal.fetchone()

    def build_hierachy(self):
        # find free nodes
        # for each node iterate through all aspects list pairs with this node
        # add as children those whose semantic distance is less them average distance in ideal tree
        pass