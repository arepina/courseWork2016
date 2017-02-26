from sklearn.model_selection import train_test_split

from aspects.Aspects import Aspects
from aspects.Context import Context
from aspects.DB import DB
from aspects.IdealAspectsDB import IdealAspectsDB
from aspects.Lexical import Lexical
from aspects.OneClassSVM import OneClassSVM
from aspects.PMI import PMI
from aspects.SemanticDistanceLearning import SemanticDistanceLearning
from aspects.Sentence import Sentence
from aspects.Splitter import Splitter
from aspects.Syntactic import Syntactic


class Main:
    vocabulary = None
    db = None
    aspect = None

    def __init__(self):
        self.db = DB()  # data base
        self.aspect = Aspects()
        # self.aspects_process()
        # self.sentence_process()
        # self.split_process()
        self.pmi_process()
        # self.semantic_learning_process()
        # self.contextual_features()
        # self.lexical_features()
        self.syntactic_features()

    def aspects_process(self):
        self.aspect.process(self.aspect, self.db)  # find aspects with the help of ISP RAS API
        # clean the data with the help of unnecessary class
        one_class_svm = OneClassSVM()
        data = one_class_svm.get_data(self.db)  # get only aspects from data base
        # get labels for all the aspects depends on their ideality
        labels = one_class_svm.get_labels(data, self.db)
        # split the data (80% for training)
        train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)
        # unarray the 2D arrays and make them 1D
        test_data_unarrayed = one_class_svm.unarray(test_data)
        train_data_unarrayed = one_class_svm.unarray(train_data)
        train_labels_unarrayed = one_class_svm.unarray(train_labels)
        # get only ideal aspects from aspects list (label = 1) for train data
        train_data_unarrayed = one_class_svm.get_ideal_data(train_data_unarrayed, train_labels_unarrayed)
        # train the one-class SVM and predict the aspects
        test_labels_unarrayed = one_class_svm.train_and_predict(train_data_unarrayed, test_data_unarrayed)
        # get only ideal aspects from aspects list (label = 1) for test data
        test_data_unarrayed = one_class_svm.get_ideal_data(test_data_unarrayed, test_labels_unarrayed)
        # now the sum of test_data_unarrayed and train_data_unarrayed have only ideal aspects
        ideal_aspects = test_data_unarrayed + train_data_unarrayed
        ideal = IdealAspectsDB()
        ideal.count_aspects()  # number of ideal aspects
        # got only ideal aspects in the db
        self.aspect.move_ideal_aspects(ideal, ideal_aspects, self.db)
        # clean the data with the help of unnecessary class
        # synonyms = Synonyms()
        # synonyms.find_synonyms(ideal)  # find and group the synonyms

    def sentence_process(self):
        sentence = Sentence()
        sentence.process(self.db, self.aspect)  # create a db with all sentences from reviews

    def split_process(self):
        sp = Splitter()  # split the words with multiple _
        sp.process_reviews(self.db)
        sp.process_sentences(self.db)

    def pmi_process(self):
        pmi = PMI()
        # reviews_corpus = pmi.get_all_reviews_corpus(self.db)  # reviews
        # sentences_corpus = pmi.get_all_sentences_corpus(self.db)  # sentences
        # pmi_ideal(pmi, reviews_corpus, sentences_corpus)  # ideal
        self.vocabulary = pmi.get_vocabulary(self.db)
        # self.pmi_review(pmi, reviews_corpus, self.vocabulary)
        # self.pmi_sentence(pmi, sentences_corpus, self.vocabulary)

    def pmi_review(self, pmi, reviews_corpus, vocabulary):
        self.db.create_pmi_review_db()
        pmi.calculate_pmi(reviews_corpus, 0, vocabulary, self.db)
        self.db.conn_pmi_review.commit()
        pmi.move_pmi_review_db_to_file(self.db)

    def pmi_sentence(self, pmi, sentences_corpus, vocabulary):
        self.db.create_pmi_sentence_db()
        pmi.calculate_pmi(sentences_corpus, 1, vocabulary, self.db)
        self.db.conn_pmi_sentence.commit()

    def pmi_ideal(self, pmi, reviews_corpus, sentences_corpus):
        self.db.create_pmi_ideal_review_db()
        self.db.create_pmi_ideal_sentence_db()
        pmi.iterate_ideal_aspects_files(pmi, reviews_corpus, sentences_corpus, self.db)

    def semantic_learning_process(self):
        semantic_learning = SemanticDistanceLearning()
        # self.db.create_path_weight_db()
        # semantic_learning.calculate_ground_truth_distance(self.db)
        self.db.create_semantic_distance_db()
        semantic_learning.process_semantic_distance_learning(self.db)

    def contextual_features(self):
        context = Context()
        context.process(self.db, self.vocabulary)

    def lexical_features(self):
        lexical = Lexical()
        lexical.process(self.vocabulary, self.db)

    def syntactic_features(self):
        syntactic = Syntactic()
        syntactic.process(self.db, self.vocabulary, self.aspect)

main = Main()


# Sizes data
# len(data, labels) = 24093
# len(train_data, train_labels) = 19274
# len(test_data, test_labels) = 4819
# len(train_data_unarrayed) = 619286
# len(test_data_unarrayed) = 154951
# len(all_aspects) = 774237
# len(ideal_train_data_unarrayed) = 46149
# len(ideal_test_data_unarrayed) = 124709
# len(ideal_aspects_dictionary) = 170858
# len(ideal_aspects) = 540571
# len(grouped aspects) = 421715
# len(vocabulary) = 45435
# len(pmi_review) = 1 032 146 895
