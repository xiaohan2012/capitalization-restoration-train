# Logistic regression is used for this task, instead of sequence model
import codecs
import numpy as np
import pickle
from itertools import chain

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import (classification_report, accuracy_score,
                             precision_recall_fscore_support)

from scipy_util import (load_sparse_csr, save_sparse_csr)

from util import load_crfsuite_format_data

from sklearn.grid_search import GridSearchCV

# turn this ON when you want to rebuild the data matrices
LOAD_FROM_CACHE = 1

# Data preparation

if not LOAD_FROM_CACHE:
    train_path = "/cs/taatto/home/hxiao/capitalization-recovery/result/feature/cap/1+2+3+4+5+6/train.crfsuite.txt"
    test_path = "/cs/taatto/home/hxiao/capitalization-recovery/result/feature/cap/1+2+3+4+5+6/test.crfsuite.txt"

    train_x, train_y = load_crfsuite_format_data(
        codecs.open(train_path, 'r', 'utf8'))
    test_x, test_y = load_crfsuite_format_data(codecs.open(test_path, 'r', 'utf8'))

    train_x, train_y = chain.from_iterable(train_x), chain.from_iterable(train_y)
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
        
else:
    print "loading data"
    train_x, test_x \
        = map(load_sparse_csr, ('cached_data/train_x.npz',
                                'cached_data/test_x.npz'))
    train_y = np.load('cached_data/train_y.npy')
    test_y = np.load('cached_data/test_y.npy')
    labels = pickle.load(open('cached_data/labels.pkl', 'r'))

# Train
print "training model"

# model = LogisticRegression(verbose=2)
model = svm.SVC()

# param_grid = {'penalty': ['l1', 'l2'],
#               'C': [0.1, 1, 10]}
param_grid = {'kernel': ('linear', 'rbf'),
              'C': [1, 10]}

grid_model = GridSearchCV(model, param_grid=param_grid, verbose=2, n_jobs=12)

grid_model.fit(train_x, train_y)
print grid_model

pred_y = grid_model.predict(test_x)

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


p_mac, r_mac, f_mac, _ = precision_recall_fscore_support(test_y, pred_y,
                                                         average="macro")

print "Precision/Recall/F1(macro) : %.4f  %.4f  %.4f\n" \
    % (p_mac, r_mac, f_mac)


p_mic, r_mic, f_mic, _ = precision_recall_fscore_support(test_y, pred_y,
                                                         average="micro")

print "Precision/Recall/F1(micro) : %.4f  %.4f  %.4f\n" \
    % (p_mic, r_mic, f_mic)

