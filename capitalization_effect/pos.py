import nltk
from nltk.tag import pos_tag
from nltk.tag.stanford import POSTagger
from nltk.data import load

from sklearn import metrics
import pdb


nltk.internals.config_java(options='-Xmx4096M')


def main(word_transformation = None):
    tagger = POSTagger('/cs/fs/home/hxiao/code/CoreNLP/classes/edu/stanford/nlp/models/pos-tagger/english-left3words/english-bidirectional-distsim.tagger',
                       '/cs/fs/home/hxiao/code/CoreNLP/javanlp-core.jar')
    
    tagged_corpus = nltk.corpus.brown.tagged_sents()[-1000:]
    
    print "extracting sentence words"
    if word_transformation and callable(word_transformation):
        tagged_corpus = [[(word_transformation(w), t) for w,t in sent]
                         for sent in tagged_corpus]

    print "extracting sents/tags"
    sents = ([w for w,t in sent]
             for sent in tagged_corpus)
    
    correct_tags = [[t for w,t in sent]
                    for sent in tagged_corpus]
    
    print "predicting"
    predicted_tags = [[t for w,t in tagger.tag(sent)]
                      for sent in sents]
    
    print "reporting"
    report = metrics.classification_report(correct_tags, predicted_tags)
    print report.split('\n')[-2]

if __name__ == "__main__":
    import sys
    try:
        oper = sys.argv[1]
        if oper == "upper":
            print "using `upper`"
            main(lambda s: s.upper())
        if oper == "cap":
            print "using `cap`"
            main(lambda s: s.title())
        elif oper == "lower":
            print "using `lower`"
            main(lambda s: s.lower())
        else:
            print "invalid oper"
    except IndexError:
        main()
