from aspects.Aspects import Aspects
from aspects.DB import DB
from aspects.PMI import PMI

db = DB()  # data base
aspect = Aspects()
# aspect.process(aspect, db)  # find aspects with the help of ISP RAS API
# clean the data with the help of unnecessary class
# one_class_svm = OneClassSVM()
# data = one_class_svm.get_data(db)  # get only aspects from data base
# # get labels for all the aspects depends on their ideality
# labels = one_class_svm.get_labels(data, db)
# # split the data (80% for training)
# train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2)
# # unarray the 2D arrays and make them 1D
# test_data_unarrayed = one_class_svm.unarray(test_data)
# train_data_unarrayed = one_class_svm.unarray(train_data)
# train_labels_unarrayed = one_class_svm.unarray(train_labels)
# # get only ideal aspects from aspects list (label = 1) for train data
# train_data_unarrayed = one_class_svm.get_ideal_data(train_data_unarrayed, train_labels_unarrayed)
# # train the one-class SVM and predict the aspects
# test_labels_unarrayed = one_class_svm.train_and_predict(train_data_unarrayed, test_data_unarrayed)
# # get only ideal aspects from aspects list (label = 1) for test data
# test_data_unarrayed = one_class_svm.get_ideal_data(test_data_unarrayed, test_labels_unarrayed)
# # now the sum of test_data_unarrayed and train_data_unarrayed have only ideal aspects
# ideal_aspects = test_data_unarrayed + train_data_unarrayed
# ideal.count_aspects()  # number of idel aspects
# # got only ideal aspects in the db
# aspect.move_ideal_aspects(ideal, ideal_aspects)
# clean the data with the help of unnecessary class
# synonyms = Synonyms()
# synonyms.find_synonyms(ideal)  # find and group the synonyms
# sentence = Sentence(db)
# sentence.process(db, aspect)  # create a db with all sentences from reviews
# sp = Splitter()  split the words with multiple _
# sp.process_reviews()
# sp.process_sentences()
pmi = PMI()
# reviews_corpus = pmi.get_all_reviews_corpus(db)  # reviews
sentences_corpus = pmi.get_all_sentences_corpus(db)  # sentences
# ideal_aspects_from_train_files = pmi.get_all_ideal_aspects_from_train_files()
# start = datetime.now()  # ideal aspects from file + reviews
# print(start)
# db.create_pmi_ideal_review_db()
# pmi.calculate_pmi_review(reviews_corpus, 2, ideal_aspects_from_train_files, db)
# db.conn_pmi_ideal_review.commit()
# print(datetime.now() - start)
# start = datetime.now()  # ideal aspects from file + sentences
# print(start)
# db.create_pmi_ideal_sentence_db()
# pmi.calculate_pmi_review(sentences_corpus, 3, ideal_aspects_from_train_files, db)
# db.conn_pmi_ideal_sentence.commit()
# print(datetime.now() - start)
vocabulary = pmi.get_vocabulary(db)
# db.create_pmi_review_db()
# pmi.calculate_pmi_review(reviews_corpus, 0, vocabulary, db)
# db.conn_pmi_review.commit()
db.create_pmi_sentence_db()
pmi.calculate_pmi_sentence(sentences_corpus, vocabulary, db)
db.conn_pmi_sentence.commit()
# semantic_learning = SemanticDistanceLearning()
# db.create_path_weight_db()
# semantic_learning.calculate_ground_truth_distance(db)

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
# len(pmi_review) = 1032146895
