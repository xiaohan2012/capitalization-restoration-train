import nltk
from nltk.tree import Tree
from nltk.corpus import conll2000

import pdb

class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)

def convert_leaf_node(t, convert_func):
    """

    >>> from nltk.tree import Tree
    >>> t = Tree(1, [2, Tree(3, [4]), 5])
    >>> t = convert_leaf_node(t, lambda v: v-1)
    >>> print(t)
    (1 1 (3 3) 4)
    """
    if isinstance(t, Tree):
        return Tree(t.label(), [convert_leaf_node(child, convert_func) for child in t])
    else:
        return convert_func(t)

class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        from nltk.classify import megam
        megam.config_megam(bin='/cs/fs/home/hxiao/code/megam_i686.opt')
        self.classifier = nltk.MaxentClassifier.train(
           train_set, algorithm='megam', trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)

def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    return {"pos": pos}


def main(convert_func = None):        
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])

    if convert_func:
        # transform the sentence
        test_sents = [convert_leaf_node(sent, convert_func) 
                      for sent in test_sents]

    unigram_chunker = UnigramChunker(train_sents)

    print(unigram_chunker.evaluate(test_sents))

if __name__ == "__main__":
    # main()
    # convert_func = lambda (s,t): (s.lower(), t)
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    chunker = ConsecutiveNPChunker(train_sents)
    print(chunker.evaluate(test_sents))



