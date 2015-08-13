import nltk
import json
from codecs import open
import logging

logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s',
                    level = logging.INFO)

from cap_transform import (make_capitalized_title, make_uppercase_title, make_lowercase_title)
from data import get_label


def evaluate(predicate_func,
             title_transformation_func,
             title_file_path="reuters.txt",
             doc_data_dir="/cs/puls/tmp/Capitalization/reuters-text",
             pass_doc=False):
    # Head word title should be different for monocase
    total_correct_n = 0.
    total_n = 0

    logging.info("Evaluation of %r starts..", predicate_func)
    
    with open(title_file_path, "r", "utf8") as f:
        total_instance_number = 10000.
        finished_instance_number = 0;
        for l in f:
            if finished_instance_number == total_instance_number:
                break

            fname, raw_title = json.loads(l)
            
            raw_words = nltk.word_tokenize(raw_title)

            try:
                cap_words = title_transformation_func(title_words = raw_words)
            except:
                logging.error("%s encountered error in making capitalized title." %(fname))
                traceback.print_exc(file=sys.stdout)
                continue
            
            if pass_doc:
                with open("%s/%s" %(doc_data_dir, fname), "r", "utf8") as f:
                    kwargs = {"doc": f.read()}
            else:
                kwargs = {}
                    
            normalized_words = predicate_func(words = cap_words, **kwargs)
            
            correct_labels = [get_label(w)
                              for w in raw_words]
            try:
                predicted_labels = [get_label(w)
                                    for w in normalized_words]
            except:
                logging.error("%s encountered error in recovery." %(fname))
                traceback.print_exc(file=sys.stdout)
                continue
                
            total_correct_n += len(filter(lambda (rw, nw): rw == nw, zip(raw_words, normalized_words)))
            total_n += len(correct_labels)

            finished_instance_number += 1
            
            if finished_instance_number % 1000 == 0:
                logging.info("%f finished", finished_instance_number / total_instance_number)

    print total_correct_n / total_n

if __name__  == "__main__":
    # from baseline1 import normalize_title as b1
    # from baseline2 import normalize_title as b2
    from baseline3 import normalize_title as b3
    # evaluate(predicate_func = b2, pass_doc = True)
    # evaluate(predicate_func = b1)
    evaluate(predicate_func=b3, 
             title_transformation_func=make_capitalized_title,
             pass_doc=True)

