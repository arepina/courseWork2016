from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor


class EnsembleClassifier:
    def __init__(self):
        # self.model = RandomForestClassifier(criterion='entropy', max_depth=8, min_samples_leaf=10, n_estimators=250)
        self.model = RandomForestRegressor(criterion='mse', max_depth=8, min_samples_leaf=10, n_estimators=250)

    def process(self,x_test):#, x_train, y_train):  # x_train - characteristic(6 item), y_train - semantic distance
        # self.model.fit(x_train, y_train)
        from sklearn.externals import joblib
        # joblib.dump(self.model, "train_dump.pkl")
        self.model = joblib.load("train_dump.pkl")
        return self.model.predict(x_test)

    @staticmethod
    def get_train(db):
        row_review_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence_ideal = db.cursor_pmi_ideal_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical_ideal = db.cursor_lexical_ideal.execute('SELECT * FROM Lexical').fetchone()
        count = 0
        x_train = []
        y_train = []
        row = db.cursor_path_weight.execute('SELECT * FROM Weight').fetchone()
        while row_review_ideal is not None:
            print(count)
            count += 1
            pmi_review = float(row_review_ideal[5])
            pmi_sentence = float(row_sentence_ideal[5])
            lexical = int(row_lexical_ideal[2])
            aspect1 = row_lexical_ideal[0].replace("_", " ")
            aspect2 = row_lexical_ideal[1].replace("_", " ")
            # local
            row_local_ideal = db.cursor_local_context_ideal.execute(
                'SELECT * FROM Context WHERE aspect1 = ? AND aspect2 = ?',
                (aspect1, aspect2,)).fetchone()
            try:
                local_context = float(row_local_ideal[2])
            except:  # we can have (1,0) or (0,1) so need to find the correct one
                row_local_ideal = db.cursor_local_context_ideal.execute(
                    'SELECT * FROM Context WHERE aspect1 = ? AND aspect2 = ?',
                    (aspect2, aspect1,)).fetchone()
                local_context = float(row_local_ideal[2])
            # global
            row_global_ideal = db.cursor_global_context_ideal.execute(
                'SELECT * FROM Context WHERE aspect1 = ? AND aspect2 = ?',
                (aspect1, aspect2,)).fetchone()
            try:
                global_context = float(row_global_ideal[2])
            except:  # we can have (1,0) or (0,1) so need to find the correct one
                row_global_ideal = db.cursor_global_context_ideal.execute(
                    'SELECT * FROM Context WHERE aspect1 = ? AND aspect2 = ?',
                    (aspect2, aspect1,)).fetchone()
                global_context = float(row_global_ideal[2])
            # syntactic
            row_syntactic_ideal = db.cursor_syntactic_ideal.execute(
                'SELECT * FROM Syntactic WHERE aspect1 = ? AND aspect2 = ?',
                (row_lexical_ideal[0], row_lexical_ideal[1],)).fetchone()
            try:
                syntactic = int(row_syntactic_ideal[2])
            except:  # we can have (1,0) or (0,1) so need to find the correct one
                row_syntactic_ideal = db.cursor_syntactic_ideal.execute(
                    'SELECT * FROM Syntactic WHERE aspect1 = ? AND aspect2 = ?',
                    (row_lexical_ideal[1], row_lexical_ideal[0],)).fetchone()
                syntactic = int(row_syntactic_ideal[2])
            if syntactic == -1:
                syntactic = 0
            x_train.append([pmi_review, pmi_sentence, lexical, syntactic, local_context, global_context])
            y_train.append(row[3])
            row = db.cursor_path_weight.fetchone()
            row_review_ideal = db.cursor_pmi_ideal_review.fetchone()
            row_sentence_ideal = db.cursor_pmi_ideal_sentence.fetchone()
            row_lexical_ideal = db.cursor_lexical_ideal.fetchone()
        return x_train, y_train

    @staticmethod
    def get_test(db):
        row_review = db.cursor_pmi_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence = db.cursor_pmi_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical = db.cursor_lexical.execute('SELECT * FROM Lexical').fetchone()
        row_syntactic = db.cursor_syntactic.execute('SELECT * FROM Syntactic').fetchone()
        row_local = db.cursor_local_context.execute('SELECT * FROM Context').fetchone()
        row_global = db.cursor_global_context.execute('SELECT * FROM Context').fetchone()
        count = 0
        x_test = []
        while row_review is not None:
            print(count)
            count += 1
            pmi_review = float(row_review[5])
            pmi_sentence = float(row_sentence[5])
            lexical = int(row_lexical[2])
            syntactic = int(row_syntactic[2])
            local_context = float(row_local[2])
            global_context = float(row_global[2])
            x_test.append([pmi_review, pmi_sentence, lexical, syntactic, local_context, global_context])
            row_review = db.cursor_pmi_review.fetchone()
            row_sentence = db.cursor_pmi_sentence.fetchone()
            row_lexical = db.cursor_lexical.fetchone()
            row_local = db.cursor_local_context.fetchone()
            row_global = db.cursor_global_context.fetchone()
        return x_test
