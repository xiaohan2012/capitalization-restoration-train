import nltk
from collections import (defaultdict, Counter)

from cap_transform import (make_lowercase_title, make_uppercase_title, make_capitalized_title)
from data import load_labeled_data
from cap_transform import transform_data
from sklearn.metrics import classification_report

class OneGramCapitalizer(object):
    """
    The majority-wining capitalizer:

    Choose the most frequent label for the word observed the training set, 
    If the word is unknown, choose the most frequent label across all words
    
    >>> training_data = [[("Google", "IC"), ("IBM", "AU"), ("this", "AL"), ("directX", "MX")], [("This", "IC"), ("this", "AL"), (",", "AN"), ("Google", "IC")], [("is", "AL"), ("but", "AL")]]
    >>> c = OneGramCapitalizer(training_data)
    >>> c.predict("THIS IS GOOGLE .INC AND , DIRECTX IBM")
    ['IC', 'AL', 'IC', 'AL', 'AL', 'AN', 'MX', 'AU']

    """
    def __init__(self, training_data):
        self.word_label_freq, self.label_freq = self._get_stat(training_data)

    def _get_stat(self, labeled_sents):
        """
        labeled_sents: list of list of tuple(word, label)
        """
        word_label = defaultdict(Counter)
        labels = Counter()
        
        for sent in labeled_sents:
            for word, label in sent:
                word_label[word.lower()][label] += 1
                labels[label] += 1

        return word_label, labels

    def predict_word(self, word):
        label, _ = self.word_label_freq.get(word.lower(), self.label_freq).most_common(n=1)[0]

        return label

    def predict(self, title = "", words = [], **kwargs):
        if title:
            words = nltk.word_tokenize(title)

        labels = ['IC']
        labels += [self.predict_word(word) for word in words[1:]]
        return labels

def evaluate(train_data, test_data):

    
    print "collecting stat"
    c = OneGramCapitalizer(train_data)

    print "predicting"
    predicted_labels = [c.predict(words = [w for w,t in sent]) 
                        for sent in test_data]
    predicted_labels = [l for sent in predicted_labels for l in sent]
    
    
    correct_labels = [t for sent in test_data for _,t in sent]
    
    print "reporting"    
    print classification_report(correct_labels, predicted_labels)
    
    correct_n = len([1 
                     for p, c in zip(predicted_labels, correct_labels) 
                     if p == c])
    
    print "Item accuracy:", float(correct_n) / len(correct_labels)

if __name__ == "__main__":

    import sys
    try:
        oper = sys.argv[1]
    except IndexError:
        print "Please specify the mode"
        sys.exit(-1)

    oper_map = {
        "upper": make_uppercase_title,
        "lower": make_lowercase_title,
        "cap": make_capitalized_title
    }
    transform_func = oper_map.get(oper)
    if not transform_func:
        raise ValueError("Invalid oper")
    else:
        print "Oper: %s" %(oper)
        train_data = transform_data(list(load_labeled_data("corpus/titles_train.txt")), 
                                    transform_func)
        test_data = transform_data(list(load_labeled_data("corpus/titles_test.txt")),
                                   transform_func)

        evaluate(train_data, test_data)
