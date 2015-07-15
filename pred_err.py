"""
Get examples of prediction errors
"""
from codecs import open
from itertools import izip
from sklearn.metrics import confusion_matrix


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
    import sys
    import pycrfsuite
    
    cap_model = sys.argv[1]  # cap.model
    content_path = sys.argv[2]  # "test.txt"
    test_data_path = sys.argv[3]  # "test.crfsuite.txt"
    
    tagger = pycrfsuite.Tagger()
    tagger.open(cap_model)

    pred_y = []
    true_y = []
    
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
            correct_or_not = map(lambda (cl, pl): cl == pl,
                                 izip(correct_labels, predicted_labels))
            
            # add some high lighting
            words = [("**" + w + "**" if not flag else w)  
                     for w, flag in izip(words, correct_or_not)]
            
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

    cm = confusion_matrix(true_y, pred_y, labels=['IC', 'AL', 'AU', 'AN', 'MX'])
    import sys
    sys.stderr.write("Confusion matrix:\n")
    sys.stderr.write("{}".format(cm))
