"""
Get examples of prediction errors
"""
from codecs import open
from itertools import izip

from util import transform_words

def load_test_data(filename):
    """
    Load test data including features and label

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
    from clint.textui import colored, puts
    import pycrfsuite
    
    tagger = pycrfsuite.Tagger()
    tagger.open('cap.model')
    
    for words, s in izip(load_sents("test.txt"), load_test_data("test.crfsuite.txt")):
        correct_labels = [l for _, l in s]

        features = [f for f,_ in s]
        predicted_labels = tagger.tag(features)
        
        if correct_labels != predicted_labels:
            correct_or_not = map(lambda (cl, pl): cl == pl, izip(correct_labels, predicted_labels))
            
            words = [("**" + w + "**" if not flag else w) #add some high lighting
                     for w,flag in izip(words, correct_or_not)]
            
            max_widths = [max([len(w), len(cl), len(pl)]) for w, cl, pl in izip(words, correct_labels, predicted_labels)]
            
            
            print '-' * (sum(max_widths) + len(max_widths))

            def style_content(c,w): 
                return c.rjust(w/2).ljust(w)
                
                    
            print "Sentence:   ", ' '.join([style_content(word, width) for width, word in zip(max_widths, words)]).encode("utf8")
            print "Correct:    ", ' '.join([style_content(cl, width) for width, cl in zip(max_widths, correct_labels)]).encode("utf8")
            print "Predicted:  ", ' '.join([style_content(pl, width) for width, pl in zip(max_widths, predicted_labels)]).encode("utf8")
            
            
            
            
        
                

