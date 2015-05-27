"""
Eval pos,parse,ner experiment result
"""

from cPickle import load
from sklearn.metrics import (confusion_matrix, classification_report, precision_recall_fscore_support)


def error_count(ctags, ptags):
    return len(filter(lambda (ctag, ptag): ctag != ptag, zip(ctags, ptags)))

def print_summary(correct, predicted, sentences, error_instances = 10):
    # flatten them
    assert len(correct) == len(predicted)
    for i, (c, p) in enumerate(zip(correct, predicted)):
        assert len(c) == len(p), "the %dth sentence,len(%r) != len(%r)" %(i, c, p)

    print "Error instances:"
    count = 1
    for sent, ctags, ptags in zip(sentences, correct, predicted):
        if count > error_instances:
            break
        ec = error_count(ctags, ptags)
        if ec == 0:
            continue

        count += 1
               
        contents = [
            (("%s_%s" %(w, ctag), ("%s_%s" %(w, ptag)))
             if ctag == ptag 
             else
             ("*%s_%s*" %(w, ctag), ("*%s_%s*" %(w, ptag))))
            for w, ctag, ptag in zip(sent, ctags, ptags)
        ]

        cc, pc = zip(*contents)
        
        print "#error: %d" %(ec)
        print " ".join(cc)
        print " ".join(pc)

    predicted = [t for row in predicted for t in row]
    correct = [t for row in correct for t in row]


    print "Confusion matrix:"
    print "-"*20
    print confusion_matrix(correct, predicted)

    print "Scores:"
    print "-"*20
    print classification_report(correct, predicted)

    print "weighted precision, recall and f1 score"
    print precision_recall_fscore_support(correct, predicted, average = "weighted")

    
def main():
    import sys
    try:
        group = sys.argv[1]
    except IndexError:
        print "give me either pos, parse or ner"
        sys.exit(-1)
        
    modes = (None, "cap", "upper", "lower")

    for mode in modes:
        if mode:
            gold, pred, sents = load(open("dumps/%s_result_%s.pkl" %(group, mode)))
        else:
            gold, pred, sents = load(open("dumps/%s_result.pkl" %(group)))
        
        print "#"*10
        print mode
        print "#"*10
        
        print_summary(gold, pred, sents)
        
        raw_input("Press key to continue")

if __name__ == "__main__":
    main()
