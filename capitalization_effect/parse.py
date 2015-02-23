import nltk
from nltk.parse.stanford import StanfordParser
from nltk.corpus import treebank
from nltk.tree import Tree

import pdb

nltk.internals.config_java("/cs/fs/home/hxiao/software/jre1.8.0_31/bin/java")
nltk.internals.config_java(options='-Xmx4096M')

def main(transform_func = None):
    parser=StanfordParser(
        path_to_jar = "/cs/fs/home/hxiao/code/stanford-parser-full-2015-01-30/stanford-parser.jar",
        path_to_models_jar = "/cs/fs/home/hxiao/code/stanford-parser-full-2015-01-30/stanford-parser-3.5.1-models.jar",
        model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
    )

    test_sents = treebank.sents()[-5000:]

    print "len(test_sents) = %d" %(len(test_sents))

    if transform_func and callable(transform_func):
        print "transforming it using ", transform_func
        test_sents = [[transform_func(w) for w in s] 
                      for s in test_sents]# transform it

    print "predicting"
    pred_parses = parser.parse_sents(test_sents)
    
    gold_parses = treebank.parsed_sents()
    
    print "evaluating"
    print precision_and_recall(
        (get_nodes_with_range(t) for t in gold_parses),
        (get_nodes_with_range(t) for t in pred_parses)
    )

    # Evaluation metric
    # https://d396qusza40orc.cloudfront.net/nlp/slides/Parsing-08-Constituency-Evaluation.pdf

def get_nodes_with_range(tree):
    """
    >>> t = Tree('A', [Tree('B', [1, 2]), Tree('C', [3, 4])])
    >>> nodes = get_nodes_with_range(t)
    >>> print sorted(nodes)
    [(1, 0, 1), (2, 1, 2), (3, 2, 3), (4, 3, 4), ('A', 0, 4), ('B', 0, 2), ('C', 2, 4)]
    """
    def find_range(t, start, nodes):
        if isinstance(t, Tree):
            acc = start
            for c in t:
                node_start, node_end = find_range(c, acc, nodes)
                acc += (node_end - node_start)                
            nodes.append((t.label(), start, acc))
            return start, acc
        else:
            nodes.append((t, start, start+1))
            return start, start+1

    nodes = []            
    find_range(tree, 0, nodes)
    return nodes

def precision_and_recall(gold_nodes_list, pred_nodes_list):
    """
    >>> gold_nodes_list = [[('S', 0, 11), ('NP', 0, 2), ('VP', 2, 9), ('VP', 3, 9), ('NP', 4, 6), ('PP', 6, 9), ('NP', 7, 9), ('NP', 9, 10)], [('S', 0, 11), ('NP', 0, 2)]]
    >>> pred_nodes_list = [[('S', 0, 11), ('NP', 0, 2), ('VP', 2, 10), ('VP', 3, 10), ('NP', 4, 6), ('PP', 6, 10), ('NP', 7, 10)], [('S', 0, 9), ('NP', 0, 2), ('SP', 0, 3)]]
    >>> p, r = precision_and_recall(gold_nodes_list, pred_nodes_list)
    >>> print (p, r)
    (0.4, 0.4)
    """
    
    gold_n = 0
    pred_n = 0
    correct_n = 0
    for gnodes, pnodes in zip(gold_nodes_list, pred_nodes_list):
        gold_n += len(gnodes)
        pred_n += len(pnodes)

        correct_n += len(set(gnodes).intersection(set(pnodes)))

    return float(correct_n) / pred_n, float(correct_n) / gold_n

if __name__ == "__main__":
    import sys
    try:
        oper = sys.argv[1]
        if oper == "upper":
            main(lambda s: s.upper())
        elif oper == "lower":
            main(lambda s: s.lower())
        elif oper == "cap":
            main(lambda s: s.title())
        else:
            print "invalid oper"
    except IndexError:
        main()
