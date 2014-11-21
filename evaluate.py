import nltk
import json
from codecs import open

from util import make_capitalized_title
from data import get_label


def evaluate(predicate_func, title_file_path = "fnames_and_titles.txt", pass_doc = False):
    
    total_correct_n = 0.
    total_n = 0
    
    with open(title_file_path, "r", "utf8") as f:
        for l in f:
            fname, raw_title = json.loads(l)
            
            raw_words = nltk.word_tokenize(raw_title)
            
            cap_words = make_capitalized_title(title_words = raw_words)
            
            if pass_doc:
                with open(fname, "r", "utf8") as f:
                    kwargs = {"doc": f.read()}
            else:
                kwargs = {}
                    
            normalized_words = predicate_func(words = cap_words, **kwargs)
            
            correct_labels = [get_label(w) for w in raw_words]
            predicted_labels = [get_label(w) for w in normalized_words]
            
            total_correct_n += len(filter(lambda (rw, nw): rw == nw, zip(raw_words, normalized_words)))
            total_n += len(correct_labels)

    print total_correct_n / total_n

if __name__  == "__main__":
    from baseline1 import normalize_title as b1
    from baseline2 import normalize_title as b2
    evaluate(predicate_func = b2, pass_doc = True)
    evaluate(predicate_func = b1)

