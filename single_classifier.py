# Logistic regression is used for this task, instead of sequence model
import codecs
import numpy as np
import pickle
from itertools import (chain, izip)
import pandas as pds

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, accuracy_score,
                             precision_recall_fscore_support,
                             confusion_matrix)
from sklearn import cross_validation
from sklearn.externals import joblib
from sklearn.grid_search import GridSearchCV

from scipy_util import (load_sparse_csr, save_sparse_csr)

from util import load_crfsuite_format_data
from unigram import UnigramLabeler

from error_display import print_label_error

# turn this ON when you want to rebuild the data matrices
LOAD_FROM_CACHE = 1
RETRAIN_MODEL = 1
ERROR_REPORT = 0

# Data preparation

train_path = "/cs/taatto/home/hxiao/capitalization-recovery/result/puls-100k/train.crfsuite.txt"
test_path = "/cs/taatto/home/hxiao/capitalization-recovery/result/puls-100k/test.crfsuite.txt"

if not LOAD_FROM_CACHE:
    train_x, train_y = load_crfsuite_format_data(
        codecs.open(train_path, 'r', 'utf8'))
    test_x, test_y = load_crfsuite_format_data(
        codecs.open(test_path, 'r', 'utf8'))

    train_x, train_y = (chain.from_iterable(train_x),
                        chain.from_iterable(train_y))

    # Debugging Purpose
    # n = 100
    # train_x = list(train_x)[:n]
    # train_y = list(train_y)[:n]

    test_x, test_y = chain.from_iterable(test_x), chain.from_iterable(test_y)
    
    print "hashing the features"
    dict_vect = DictVectorizer()

    train_x = dict_vect.fit_transform(train_x)
    test_x = dict_vect.transform(test_x)

    print "encoding the labels"
    label_encoder = LabelEncoder()
    # import pdb
    # pdb.set_trace()
    train_y = label_encoder.fit_transform(list(train_y))
    test_y = label_encoder.transform(list(test_y))

    labels = label_encoder.classes_
    
    for fname, obj in zip(
            ['cached_data/train_x.npz',
             'cached_data/test_x.npz'],
            (train_x, test_x)):
        save_sparse_csr(fname, obj)
    for fname, obj in zip(['cached_data/train_y.npy',
                           'cached_data/test_y.npy'],
                          (train_y, test_y)):
        np.save(fname, obj)
    pickle.dump(labels, open('cached_data/labels.pkl', 'w'))

    # Dump DictVectorizer and LabelEncoder
    pickle.dump(dict_vect, open('cached_data/dict_vect.pkl', 'w'))
    pickle.dump(label_encoder, open('cached_data/label_encoder.pkl', 'w'))
        
else:
    print "loading data"
    train_x, test_x \
        = map(load_sparse_csr, ('cached_data/train_x.npz',
                                'cached_data/test_x.npz'))
    train_y = np.load('cached_data/train_y.npy')
    test_y = np.load('cached_data/test_y.npy')
    labels = pickle.load(open('cached_data/labels.pkl', 'r'))
    
    dict_vect = pickle.load(open('cached_data/dict_vect.pkl', 'r'))
    label_encoder = pickle.load(open('cached_data/label_encoder.pkl', 'r'))

# print(train_x.shape)
# # print(train_x[0])

if RETRAIN_MODEL:
    # Train
    train_x, test_x, train_y, test_y = cross_validation.train_test_split(
        train_x,
        train_y,
        test_size=0.1,
        random_state=0)

    print(train_x.shape)
    print(train_y.shape)
    print(test_x.shape)
    print(test_y.shape)

    print "training model"
    model = LogisticRegression(penalty='l2',
                               C=1.0,
                               verbose=2)

    # Uncomment when you want grid search
    # param_grid = {'penalty': ['l1', 'l2'],
    #               'C': [0.1, 1, 10]}
    # model = GridSearchCV(LogisticRegression(verbose=2), param_grid=param_grid,
    #                      verbose=2, n_jobs=6)

    model.fit(train_x, train_y)
    print model

    pred_y = model.predict(test_x)

    # Evaluation
    print "Evaluation summary:"

    print "Subset accuracy: %.2f\n" % \
        (accuracy_score(test_y, pred_y) * 100)

    # print "Accuracy(Jaccard): %.2f\n" % (jaccard_similarity_score(test_y, pred_y))

    # p_ex, r_ex, f_ex, _ = precision_recall_fscore_support(test_y, pred_y,
    #                                                       average="samples")
    print classification_report(test_y, pred_y,
                                target_names=labels,
                                digits=4)


    p_mac, r_mac, f_mac, _\
        = precision_recall_fscore_support(test_y, pred_y,
                                          average="macro")

    print "Precision/Recall/F1(macro) : %.4f  %.4f  %.4f\n" \
        % (p_mac, r_mac, f_mac)


    p_mic, r_mic, f_mic, _\
        = precision_recall_fscore_support(test_y, pred_y,
                                          average="micro")

    print "Precision/Recall/F1(micro) : %.4f  %.4f  %.4f\n" \
        % (p_mic, r_mic, f_mic)
    
    joblib.dump(model, 'cached_data/model.pkl')

else:
    model = joblib.load('cached_data/model.pkl')


if ERROR_REPORT:
    print "Error examples"
    test_x_features, test_y = load_crfsuite_format_data(
        codecs.open(test_path, 'r', 'utf8'))
    
    labeler = UnigramLabeler(dict_vect, label_encoder, model)
    flat_pred_y = labeler.predict(chain.from_iterable(test_x_features))
    
    # unflatten the predicted labels
    pred_y = []
    current_index = 0
    for sent_y in test_y:
        pred_y.append(flat_pred_y[current_index: current_index+len(sent_y)])
        current_index += len(sent_y)
    assert len(pred_y) == len(test_x_features)

    sents = [[word['word[0]']
              for word in words]
             for words in test_x_features]

    for words, features,\
        true_labels, pred_labels in izip(sents,
                                         test_x_features, test_y, pred_y):
        print_label_error(words, features,
                          true_labels, pred_labels,
                          target_true_label='IC', target_pred_label='AL',
                          print_features=True,
                          model=model,
                          dict_vect=dict_vect,
                          label_encoder=label_encoder)

print "Confusion matrix:"
table = pds.DataFrame(confusion_matrix(list(chain.from_iterable(test_y)),
                                       list(chain.from_iterable(pred_y)),
                                       labels=labels),
                      index=map(lambda s: '{}_true'.format(s), labels),
                      columns=map(lambda s: '{}_pred'.format(s), labels))
print table


    
