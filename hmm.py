"""
This implementation is based on the HMM description in Chapter 8, Huang,
Acero and Hon, Spoken Language Processing and includes an extension for
training shallow HMM parsers or specialized HMMs as in Molina et.
al, 2002. 
"""
from nltk.tag.hmm import HiddenMarkovModelTagger
from data import load_labeled_data
from cap_transform import transform_data
from util import (make_uppercase_title, make_lowercase_title, make_capitalized_title)


def main(train_data, test_data):
    print "Training"

    m = HiddenMarkovModelTagger.train(train_data)

    print "Predicting"
    predicted_labels = []

    for i, sent in enumerate(test_data):
        if i % 500 == 0:
            print "%d / %d" %(i, len(test_data))
        predicted_labels += [tag 
                             for _, tag in m.tag(
                                     [word for word, _ in sent]
                             )]



    correct_labels = [tag 
                      for sent in test_data
                      for _, tag in sent]

    # print predicted_labels
    # print correct_labels

    from sklearn.metrics import classification_report

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
        
        main(train_data, test_data)
