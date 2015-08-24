"""
Get examples of prediction errors
"""
from codecs import open
from itertools import izip
from sklearn.metrics import confusion_matrix
from pandas import DataFrame as df
from collections import Counter
from error_display import print_label_error


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
                        help="Sentence path(test.txt)")
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
        
        print_label_error(words, features,
                          correct_labels, predicted_labels,
                          args.true_label, args.pred_label,
                          args.print_features)

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
    
