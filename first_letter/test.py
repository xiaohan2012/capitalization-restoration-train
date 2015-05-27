# coding: utf-8
import nltk
from nltk.tag.mapping import map_tag
import pprint

trees = nltk.corpus.treebank.parsed_sents()
multi_s_trees = [tree for tree in trees if len(list(tree.subtrees(lambda t: t.label() == 'S'))) > 1]

sents = [' '.join(list(t.subtrees(lambda t: t.label() == 'S'))[1].leaves()) for t in multi_s_trees]

pprint.pprint(sents)
