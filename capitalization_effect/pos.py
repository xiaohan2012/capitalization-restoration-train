import nltk
from nltk.tag import pos_tag
from nltk.data import load

from sklearn import metrics
import pdb

def main(word_transformation = None):
    _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
    tagger = load(_POS_TAGGER)
    
    tagged_corpus = nltk.corpus.brown.tagged_sents()
    
    print "extracting sentence words"
    if word_transformation and callable(word_transformation):
        sents = ([word_transformation(w) for w,t in sent]
                 for sent in tagged_corpus)
    else:
        sents = ([w for w,t in sent]
                 for sent in tagged_corpus)

    print "extracting correct tags"
    correct_tags = [[t for w,t in sent]
                    for sent in tagged_corpus]
    
    print "evaluating"
    
    predicted_tags = [[t for w,t in tagger.tag(sent)]
                      for sent in sents]

    prec = tagger.evaluate(tagged_corpus)

    report = metrics.classification_report(correct_tags, predicted_tags)
    print report.split('\n')[-2]



if __name__ == "__main__":
    import sys
    try:
        oper = sys.argv[1]
        if oper == "upper":
            main(lambda s: s.upper())
        elif oper == "lower":
            main(lambda s: s.lower())
        else:
            print "invalid oper"
    except IndexError:
        main()
