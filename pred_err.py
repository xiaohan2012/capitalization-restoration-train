"""
Get examples of prediction errors
"""
import numpy as np
from codecs import open
from itertools import izip
from sklearn.metrics import confusion_matrix
from pandas import DataFrame as df
from collections import Counter

def load_test_data(filename):
    """
    Load test data including features and label
    
    Return (list of features, label)
    """
    with open(filename, "r", "utf8") as f:
        sent = []
        for l in f:
            l = l.strip()
            if l:
                segs = l.split()
                sent.append((segs[1:], segs[0]))
            else:
                # a new sentence
                yield sent
                sent = []


def load_sents(filename):
    """
    Load sentences as lists of words
    """
    with open(filename, "r", "utf8") as f:
        sent = []
        for l in f:
            l = l.strip()
            if l:
                sent.append(l.split()[0])
            else:
                # a new sentence
                yield sent
                sent = []

if __name__ == "__main__":
    import pycrfsuite
    import argparse

    parser = argparse.ArgumentParser(description="Error analysis utility")
    parser.add_argument("--model", required=True, type=str, help="Model path")
    parser.add_argument("--sent_path", required=True, type=str,
                        help="Sentence path")
    parser.add_argument("--crfsuite_path", required=True, type=str,
                        help="Crfsuite--extracted features path")
    parser.add_argument("--true_label", required=True, type=str,
                        help="The actual value")
    parser.add_argument("--pred_label", required=True, type=str,
                        help="The predicted value")
    parser.add_argument("--features", action="store_true",
                        dest="print_features",
                        help="Print features or not")
    
    args = parser.parse_args()
    cap_model = args.model  # cap.model
    content_path = args.sent_path  # "test.txt"
    test_data_path = args.crfsuite_path  # "test.crfsuite.txt"

    labels = ['IC', 'AL', 'AU', 'AN', 'MX']
    assert args.pred_label in labels
    assert args.true_label in labels

    tagger = pycrfsuite.Tagger()
    tagger.open(cap_model)

    pred_y = []
    true_y = []
    
    word_counter = Counter()
    feature_counter = Counter()

    for words, s in izip(
            load_sents(content_path),
            load_test_data(test_data_path)):
        correct_labels = [l for _, l in s]        

        features = [f for f, _ in s]
        predicted_labels = tagger.tag(features)
        
        # all the predicted/true labels
        # used for confusion matrix
        pred_y += predicted_labels
        true_y += correct_labels
        
        if correct_labels != predicted_labels:
            # we want labels that are both 
            # incorrect and meet our label specs
            display_or_not = map(lambda (cl, pl): cl != pl and
                                 cl == args.true_label and
                                 pl == args.pred_label,
                                 izip(correct_labels, predicted_labels))
            if np.any(display_or_not):
                for w, word_features, flag in \
                    izip(words, features,
                         display_or_not):
                    if flag:
                        word_counter[w] += 1
                        for feat in word_features:
                            feature_counter[feat] += 1
                            
                # add some high lighting                
                words = [("**" + w + "**" if flag else w)  
                         for w, flag in izip(words, display_or_not)]

                word_counter
                max_widths = [max([len(w), len(cl), len(pl)]) 
                              for w, cl, pl in 
                              izip(words, correct_labels, predicted_labels)]
                
                print '-' * (sum(max_widths) + len(max_widths))

                def style_content(c, w):
                    return c.ljust(w)
                        
                print "Sentence:   ", ' '.join([style_content(word, width)
                                                for width, word in
                                                zip(max_widths, words)]).encode("utf8")
                print "Correct:    ", ' '.join([style_content(cl, width)
                                                for width, cl in
                                                zip(max_widths, correct_labels)]).encode("utf8")
                print "Predicted:  ", ' '.join([style_content(pl, width)
                                                for width, pl in
                                                zip(max_widths, predicted_labels)]).encode("utf8")
                if args.print_features:
                    print "Features:   "
                    for word_features, flag in izip(features, display_or_not):
                        if flag:
                            print word_features


    cm = confusion_matrix(true_y, pred_y,
                          labels=labels)

    table = df(cm,
               index=map(lambda s: '{}_true'.format(s), labels),
               columns=map(lambda s: '{}_pred'.format(s), labels))
    print table
    print word_counter.most_common(10)
    print feature_counter.most_common(10)
    # import sys
    # sys.stderr.write("Confusion matrix:\n")
    # sys.stderr.write("{}".format(cm))
    
