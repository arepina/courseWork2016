class OneClassSVM:

    @staticmethod
    def get_data(db):
        row = db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
        data = []
        while row is not None:  # iterate through all reviews
            aspect_arr = []
            if len(str(row[1])) != 0:
                adv = str(row[1]).split(";")
                for item in adv:
                    aspect_arr.append(item)
            if len(str(row[2])) != 0:
                dis = str(row[2]).split(";")
                for item in dis:
                    aspect_arr.append(item)
            if len(str(row[3])) != 0:
                com = str(row[3]).split(";")
                for item in com:
                    aspect_arr.append(item)
            data.append(aspect_arr)
            row = db.cursor_aspects.fetchone()
        return data

    @staticmethod
    def get_labels(data, db):
        row_review = db.cursor_reviews.execute('SELECT * FROM Review').fetchone()
        import os
        path = os.getcwd()
        train_labels = []
        count = 0
        while row_review is not None:
            subcat_name = str(row_review[1])
            file_path = path + "\\..\\productTrees\\Subcategories\\" + subcat_name + ".txt"
            ideal_labels = []
            labels = []
            with open(file_path) as f:
                ideal_labels.append(f.readlines())
            ideal_labels[0][0] = ideal_labels[0][0].lower()
            for item in data[count]:
                if item in ideal_labels[0][0]:
                    labels.append(1)
                else:
                    labels.append(-1)
            count += 1
            train_labels.append(labels)
            row_review = db.cursor_reviews.fetchone()
        return train_labels

    @staticmethod
    def get_ideal_data(data, labels):
        ideal_data = []
        for i in range(len(labels)):
            if labels[i] == 1:
                ideal_data.append(data[i])
        return ideal_data

    @staticmethod
    def unarray(data):
        unarrayed_data = []
        for i in range(len(data)):
            for item in data[i]:
                unarrayed_data.append(item)
        return unarrayed_data

    @staticmethod
    def train_and_predict(train_data, test_data):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(min_df=5,
                                     max_df=0.8,
                                     sublinear_tf=True,
                                     use_idf=True)
        train_vectors = vectorizer.fit_transform(train_data)
        test_vectors = vectorizer.transform(test_data)
        from sklearn import svm
        classifier_rbf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
        classifier_rbf.fit(train_vectors)
        prediction_rbf = classifier_rbf.predict(test_vectors)
        return prediction_rbf