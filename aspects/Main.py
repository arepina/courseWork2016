from sklearn.model_selection import train_test_split

from aspects.AllAspects import Aspects
from aspects.DB import DB
from aspects.IdealAspectsDB import IdealAspectsDB
from aspects.OneClassSVM import OneClassSVM
from aspects.PMI import PMI
from aspects.SemanticDistanceLearning import SemanticDistanceLearning
from aspects.Sentence import Sentence
from aspects.Splitter import Splitter


def aspects_process():
    aspect.process(aspect, db)  # find aspects with the help of ISP RAS API
    # clean the data with the help of unnecessary class
    one_class_svm = OneClassSVM()
    data = one_class_svm.get_data(db)  # get only aspects from data base
    # get labels for all the aspects depends on their ideality
    labels = one_class_svm.get_labels(data, db)
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
    aspect.move_ideal_aspects(ideal, ideal_aspects, db)
    # clean the data with the help of unnecessary class
    # synonyms = Synonyms()
    # synonyms.find_synonyms(ideal)  # find and group the synonyms


def sentence_process():
    sentence = Sentence()
    sentence.process(db, aspect)  # create a db with all sentences from reviews


def split_process():
    sp = Splitter()  # split the words with multiple _
    sp.process_reviews(db)
    sp.process_sentences(db)


def pmi_process():
    pmi = PMI()
    # reviews_corpus = pmi.get_all_reviews_corpus(db)  # reviews
    sentences_corpus = pmi.get_all_sentences_corpus(db)  # sentences
    # ideal_aspects_from_train_files = pmi.get_all_ideal_aspects_from_train_files()
    # start = datetime.now()  # ideal aspects from file + reviews
    # print(start)
    # db.create_pmi_ideal_review_db()
    # pmi.calculate_pmi(reviews_corpus, 2, ideal_aspects_from_train_files, db)
    # db.conn_pmi_ideal_review.commit()
    # print(datetime.now() - start)
    # start = datetime.now()  # ideal aspects from file + sentences
    # print(start)
    # db.create_pmi_ideal_sentence_db()
    # pmi.calculate_pmi(sentences_corpus, 3, ideal_aspects_from_train_files, db)
    # db.conn_pmi_ideal_sentence.commit()
    # print(datetime.now() - start)
    vocabulary = pmi.get_vocabulary(db)
    # db.create_pmi_review_db()
    # pmi.calculate_pmi(reviews_corpus, 0, vocabulary, db)
    # db.conn_pmi_review.commit()
    # pmi.move_pmi_review_db_to_file(db)
    db.create_pmi_sentence_db()
    pmi.calculate_pmi(sentences_corpus, 1, vocabulary, db)
    db.conn_pmi_sentence.commit()


def semantic_learning_process():
    semantic_learning = SemanticDistanceLearning()
    # db.create_path_weight_db()
    # semantic_learning.calculate_ground_truth_distance(db)
    db.create_semantic_distance_db()
    semantic_learning.process_semantic_distance_learning(db)


db = DB()  # data base
aspect = Aspects()
# aspects_process()
# sentence_process()
# split_process()
# pmi_process()
semantic_learning_process()


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
