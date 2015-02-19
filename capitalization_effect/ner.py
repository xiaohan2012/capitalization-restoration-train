import pdb
import nltk
from nltk.tag.stanford import NERTagger

# http://nlp.stanford.edu/software/CRF-NER.shtml
# Requires conll2003 data
tagged_corpus = nltk.corpus.conll2002.tagged_sents()

pdb.set_trace()

t = NERTagger('/cs/fs/home/hxiao/code/stanford-ner-2015-01-30/classifiers/english.all.3class.distsim.crf.ser.gz',
              '/cs/fs/home/hxiao/code/stanford-ner-2015-01-30/stanford-ner.jar')

print "extracting sentence words"
sents = ([w for w,t in sent]
         for sent in tagged_corpus)

print "extracting correct tags"
correct_tags = ([t for w,t in sent]
                for sent in tagged_corpus)

print "tagging the sentences"
tags = pt.tag_sents(sents)

pdb.set_trace()

