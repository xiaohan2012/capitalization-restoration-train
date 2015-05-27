import traceback
import nltk
from nltk.tag.stanford import POSTagger
from nltk.data import load

from sklearn import metrics
import pdb

from cPickle import dump

nltk.internals.config_java("/cs/fs/home/hxiao/software/jre1.8.0_31/bin/java")
nltk.internals.config_java(options='-Xmx8192M')

SAVE = True

def main(word_transformation = None, result_path = None, save = SAVE, n = 500):
    tagger = POSTagger('/cs/fs/home/hxiao/code/CoreNLP/classes/edu/stanford/nlp/models/pos-tagger/english-left3words/english-bidirectional-distsim.tagger',
                       '/cs/fs/home/hxiao/code/CoreNLP/javanlp-core.jar')
    
    tagged_corpus = nltk.corpus.treebank.tagged_sents()[-n:]
    
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
    predicted_tags = []
    really_correct_tags = [] # some sentence might be dropped
    sentences = []
    for i, (ctags, sent) in enumerate(zip(correct_tags, sents)):
        if (i+1) % 5 == 0:
            print "%d finished" %(i+1)
        try:
            ptags = [t for w,t in tagger.tag(sent)]
            if len(ctags) == len(ptags):
                predicted_tags.append(ptags)
                really_correct_tags.append(ctags)
                sentences.append(sent)
            else:
                print "tags length does not match for %r" %(sent)                
        except UnicodeDecodeError:
            print "UnicodeDecodeError for ", sent
        except Exception:
            traceback.print_exc()

    if save:
        print "dumping to '%s'" %(result_path)
        dump((really_correct_tags, predicted_tags, sentences), open(result_path, "w"))


if __name__ == "__main__":
    import sys
    
    try:
        oper = sys.argv[1]
        path = "dumps/pos_result_%s.pkl" %oper

        if oper == "upper":
            print "using `upper`"
            main(lambda s: s.upper(), path)
        if oper == "cap":
            print "using `cap`"
            main(lambda s: s.title(), path)
        elif oper == "lower":
            print "using `lower`"
            main(lambda s: s.lower(), path)
        else:
            print "invalid oper"
    except IndexError:
        main(result_path = "dumps/pos_result.pkl")
