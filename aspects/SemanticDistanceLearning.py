import numpy as np


class SemanticDistanceLearning:
    def calculate_ground_truth_distance(self, db):
        import os
        path = os.getcwd()
        filenames = os.listdir(path + "/../productTrees/Subcategories old")
        os.chdir(path + "/../productTrees/Subcategories")
        all_files_content = []
        for filename in filenames:  # load the aspects from all files
            with open(filename) as f:
                all_files_content.append(f.readlines())
        os.chdir(path + "/../productTrees/Subcategories old")
        count = 0
        for filename in filenames:  # iterate through all the files to calculate the path weights
            f = open(filename)
            print(filename)
            file_content = str(all_files_content[count]).split(";")  # list with ideal aspects for concrete topic
            file_content[0] = file_content[0][2:]
            file_content[len(file_content) - 1] = file_content[len(file_content) - 1][
                                                  :len(file_content[len(file_content) - 1]) - 2]
            for i in range(0, len(file_content)):
                node = file_content[i]
                for j in range(i + 1, len(file_content)):
                    next_node = file_content[j]
                    path_weight = self.find_path(node, next_node, filename)  # the min path weight between 2 words
                    db.add_path_weight(filename, node, next_node, path_weight)
                    db.conn_path_weight.commit()
            count += 1
            f.close()

    @staticmethod
    def find_path(node, next_node, filename):
        with open(filename) as f:
            content = f.readlines()
        parent_name = ""
        parent_name_next = ""
        deep_num_node = 0
        deep_num_node_next = 0
        for line in content:
            arr = line.split(";")
            word1 = arr[0]
            word2 = arr[1]
            deep_num = int(arr[2].replace("\n", ""))
            if node == word1:
                parent_name = word2
                deep_num_node = deep_num
            if next_node == word1:
                parent_name_next = word2
                deep_num_node_next = deep_num
        if len(parent_name) == 0:
            deep_num_node = 1
        if len(parent_name_next) == 0:
            deep_num_node_next = 1
        if filename.replace(".txt", "") == next_node:
            deep_num_node_next = 0
        if filename.replace(".txt", "") == node:
            deep_num_node = 0
        if parent_name == parent_name_next:
            return 2
        elif parent_name_next == node:
            return 1
        else:
            return deep_num_node + deep_num_node_next

    def calculate_distance(self, db):
        row_review_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence_ideal = db.cursor_pmi_ideal_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical_ideal = db.cursor_lexical_ideal.execute('SELECT * FROM Lexical').fetchone()
        features_arr = []
        while row_review_ideal is not None:
            pair_features = []
            pmi_r = float(row_review_ideal[5])
            pmi_s = float(row_sentence_ideal[5])
            lexical = int(row_lexical_ideal[2])
            print(row_lexical_ideal[0] + " " + row_lexical_ideal[1])
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
            pair_features.append(pmi_r)
            pair_features.append(pmi_s)
            pair_features.append(lexical)
            pair_features.append(syntactic)
            pair_features.append(local_context)
            pair_features.append(global_context)
            features_arr.append(pair_features)
            row_review_ideal = db.cursor_pmi_ideal_review.fetchone()
            row_sentence_ideal = db.cursor_pmi_ideal_sentence.fetchone()
            row_lexical_ideal = db.cursor_lexical_ideal.fetchone()
        f = np.array(features_arr)  # features's vector
        d = np.array(self.vector_with_ground_truth_distances(db))
        matrix_size = 6  # the features num
        i = np.matrix(np.identity(matrix_size))  # identity metric
        nu = 0.4
        w = np.dot(np.power(np.dot(f.T, f) + nu * i, -1), np.dot(f.T, d))
        return w  # [ -5.18461604  -7.25855391   2.49603805  -1.122215  -2.29888273 41.45422735]

    @staticmethod
    def vector_with_ground_truth_distances(db):
        row = db.cursor_path_weight.execute("SELECT * FROM Weight").fetchone()
        vector = []
        while row is not None:
            vector.append(int(row[3]))
            row = db.cursor_path_weight.fetchone()
        return vector

    def process_semantic_distance_learning(self, db):
        db.create_semantic_distance_db()
        row_review = db.cursor_pmi_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence = db.cursor_pmi_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical = db.cursor_lexical.execute('SELECT * FROM Lexical').fetchone()
        row_syntactic = db.cursor_syntactic.execute('SELECT * FROM Syntactic').fetchone()
        row_local = db.cursor_local_context.execute('SELECT * FROM Context').fetchone()
        row_global = db.cursor_global_context.execute('SELECT * FROM Context').fetchone()
        # w = np.array(self.calculate_distance(db))[0]  # will return a vector with feature values
        # w = [-7.17434844, -9.98536379, 2.89004706, -7.00041128, 102.75428241, 50.38338244, 22.32963088]  # bayes
        w = [-5.18461604, -7.25855391, 2.49603805, -1.122215, -2.29888273, 41.45422735]
        count = 0
        while row_review is not None:
            print(count)
            count += 1
            pmi_review = float(row_review[5])
            pmi_sentence = float(row_sentence[5])
            lexical = int(row_lexical[2])
            syntactic = int(row_syntactic[2])
            local_context = float(row_local[2])
            global_context = float(row_global[2])
            d = w[0] * pmi_review + w[1] * pmi_sentence + w[2] * lexical + w[3] * syntactic + w[4] * local_context + w[5] * global_context
            db.add_semantic_distance(str(row_review[0]), str(row_review[1]), d)
            row_review = db.cursor_pmi_review.fetchone()
            row_sentence = db.cursor_pmi_sentence.fetchone()
            row_lexical = db.cursor_lexical.fetchone()
            row_local = db.cursor_local_context.fetchone()
            row_global = db.cursor_global_context.fetchone()
            if count % 1000 == 0:
                db.conn_semantic_distance.commit()
        db.conn_semantic_distance.commit()

    def process_semantic_distance_learning_ideal(self, db):
        db.create_semantic_distance_ideal_db()
        row_review_ideal = db.cursor_pmi_ideal_review.execute('SELECT * FROM PMI').fetchone()
        row_sentence_ideal = db.cursor_pmi_ideal_sentence.execute('SELECT * FROM PMI').fetchone()
        row_lexical_ideal = db.cursor_lexical_ideal.execute('SELECT * FROM Lexical').fetchone()
        # w = np.array(self.calculate_distance(db))[0]  # will return a vector with feature values
        w = [-7.17434844, -9.98536379, 2.89004706, -7.00041128, 102.75428241, 50.38338244, 22.32963088] # bayes
        w = [-5.18461604, -7.25855391, 2.49603805, -1.122215, -2.29888273, 41.45422735]  # 0.4
        # [-5.18461655 - 7.25855449   2.49603811 - 1.12222121 - 2.20044153 41.45442079] 0
        # [ -5.18460385  -7.25854018   2.49603675  -1.12206601  -4.40758755  41.44959215] 10
        count = 0
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
            d = w[0] * pmi_review + w[1] * pmi_sentence + w[2] * lexical + w[3] * syntactic + w[4] * local_context + w[
                                                                                                                         5] * global_context
            db.add_semantic_distance_ideal(row_lexical_ideal[0], row_lexical_ideal[1], d)
            row_review_ideal = db.cursor_pmi_ideal_review.fetchone()
            row_sentence_ideal = db.cursor_pmi_ideal_sentence.fetchone()
            row_lexical_ideal = db.cursor_lexical_ideal.fetchone()
            db.conn_semantic_distance_ideal.commit()

    @staticmethod
    def create_semantic_distance_random_forest_classifier(db, y_test):
        db.create_semantic_distance_real_db()
        row_review = db.cursor_pmi_review.execute('SELECT * FROM PMI').fetchone()
        count = 0
        while row_review is not None:
            print(count)
            aspect1 = row_review[0]
            aspect2 = row_review[1]
            db.add_semantic_distance_real(aspect1, aspect2, y_test[count])
            row_review = db.cursor_pmi_review.fetchone()
            count += 1
        db.conn_semantic_distance_real.commit()

    @staticmethod
    def print_data(db):
        row_path_weight = db.cursor_path_weight.execute('SELECT * FROM Weight').fetchone()
        print("aspect1\t\taspect2\t\tsemantic\tweight")
        while row_path_weight is not None:
            from aspects.Context import Context
            aspect1 = Context.replacer(row_path_weight[1]).replace(" ", "_")
            aspect2 = Context.replacer(row_path_weight[2]).replace(" ", "_")
            row_semantic = db.cursor_semantic_distance_ideal.execute(
                'SELECT * FROM Distance WHERE aspect1 = ? AND aspect2 = ?',
                (aspect1, aspect2,)).fetchone()
            if row_semantic is None:
                row_semantic = db.cursor_semantic_distance_ideal.execute(
                    'SELECT * FROM Distance WHERE aspect1 = ? AND aspect2 = ?',
                    (aspect2, aspect1,)).fetchone()
            print('{:s}\t{:s}\t{:4.2f}\t{:4.2f}'.format(row_semantic[0], row_semantic[1], row_semantic[2],
                                                        float(row_path_weight[3])))
            row_path_weight = db.cursor_path_weight.fetchone()
