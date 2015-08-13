import pdb
import nltk
from nltk.tag.stanford import NERTagger
from cPickle import dump

# http://nlp.stanford.edu/software/CRF-NER.shtml
# Requires conll2003 data
from conll2003 import CoNLLNERReader

MAPPING = {
    u"I-ORG": u"ORGANIZATION", 
    u"I-PER": u"PERSON",
    u"I-LOC": u"LOCATION", 
    u"B-MISC": u"MISC",
    u"I-MISC": u"MISC",
    u"O": u"O"
}

def transform_labels(labels, mapping = MAPPING):
    return map(lambda l: mapping[l], labels)

TEST_DATA_PATH="/cs/taatto/home/hxiao/capitalization-recovery/corpus/conll2003/eng.testa"


def main(word_transformation = None, result_path = None, n = 50):
    tagged_corpus = CoNLLNERReader(TEST_DATA_PATH).read()[:n]
    
    tagger = NERTagger('/cs/fs/home/hxiao/code/stanford-ner-2015-01-30/classifiers/english.conll.4class.distsim.crf.ser.gz',
                       '/cs/fs/home/hxiao/code/stanford-ner-2015-01-30/stanford-ner.jar')

    print "extracting sentence words"
    if word_transformation and callable(word_transformation):
        tagged_corpus = [[(word_transformation(w), t) for w,t in sent]
                         for sent in tagged_corpus]

    print "extracting sents/tags"
    sents = ([w for w,t in sent]
             for sent in tagged_corpus)

    correct_tags = [transform_labels([t for w,t in sent])
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

    assert len(really_correct_tags) == len(predicted_tags), "length inconsistent"
    
    print "%d finished" %(i+1)
    
    dump((really_correct_tags, predicted_tags, sentences), open(result_path, "w"))


if __name__ == "__main__":
    import sys
    
    try:
        oper = sys.argv[1]
    except IndexError:
        main(result_path = "dumps/ner_result.pkl")
        sys.exit(0)

    path = "dumps/ner_result_%s.pkl" %oper

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

