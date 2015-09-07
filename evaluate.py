import nltk
import json
import numpy as np
import traceback

from codecs import open
from pathlib import Path


from puls_util import separate_title_from_body
from cap_transform import (make_capitalized_title,
                           make_uppercase_title,
                           make_lowercase_title)
from data import get_label
from error_display import print_label_error

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def evaluate(predicate_func,
             title_transformation_func,
             title_file_path="reuters.txt",
             doc_data_dir="/cs/puls/tmp/Capitalization/reuters-text",
             pass_doc=False):
    # Head word title should be different for monocase
    total_correct_n = 0.
    total_n = 0

    logger.info("Evaluation of %r starts..", predicate_func)
    
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
                logger.error("%s encountered error in making capitalized title." %(fname))
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
                logger.error("%s encountered error in recovery." %(fname))
                traceback.print_exc(file=sys.stdout)
                continue
                
            total_correct_n += len(filter(lambda (rw, nw): rw == nw, zip(raw_words, normalized_words)))
            total_n += len(correct_labels)

            finished_instance_number += 1
            
            if finished_instance_number % 1000 == 0:
                logger.info("%f finished", finished_instance_number / total_instance_number)

    print total_correct_n / total_n


def is_consistent_prediction(pred_tokens, true_tokens):
    """
    check if predicted label sequence is consistent
    with the actual label sequence.
    
    consistent means:

    - same length
    - same content(after lower-casing)
    """
    lower_case = lambda tokens: map(lambda t: t.lower(), tokens)
    
    if len(pred_tokens) == len(true_tokens):
        if lower_case(pred_tokens) == lower_case(true_tokens):
            return True
    return False


def eval_stat(pred_tokens, true_tokens, accepted_labels):
    ret = np.zeros((len(accepted_labels), 3))
    
    label2row = {l: i for i, l in enumerate(accepted_labels)}
    accepted_labels = set(accepted_labels)
    
    pred_tokens, true_tokens = pred_tokens[1:], true_tokens[1:]
    pred_labels = map(get_label, pred_tokens)
    true_labels = map(get_label, true_tokens)
    for i, true_l in enumerate(true_labels):
        pred_l = pred_labels[i]
        if true_l in accepted_labels and pred_l in accepted_labels:
            if pred_l == true_l:
                ret[label2row[true_l], 0] += 1
            ret[label2row[pred_l], 1] += 1
            ret[label2row[true_l], 2] += 1
            
    return ret


def eval_rule_based(output_path, okform_dir,
                    accepted_labels=set(['AL', 'IC']),
                    print_errors=False):
    """
    Return:
    numpy.ndarray: (#label, 3)
    count of #match, #mode, #ref for each label
    
    First word of sentence is ignored
    """
    ret_stat = np.zeros((len(accepted_labels), 3),
                        dtype=np.float64)
    
    n_finished = 0
    n_errorless = 0
    
    with Path(output_path).open('r', encoding='utf8') as prediction_file:
        while True:
            if n_finished % 1000 == 0:
                logger.info('Finished {}/{}'.format(n_errorless, n_finished))
                
            line1 = prediction_file.readline()
            line2 = prediction_file.readline()

            if not line2:
                break

            try:
                id_ = line1.strip()
                pred_json = json.loads(line2.strip())

                if pred_json['resultingHeadline'] is None:
                    continue

                pred_tokens = pred_json['resultingHeadline']
                
                auxil_path = str(Path(okform_dir) /
                                 Path(id_).with_suffix('.auxil'))
                paf_path = str(Path(okform_dir) /
                               Path(id_).with_suffix('.paf'))
                
                title_sents, _ = separate_title_from_body(auxil_path, paf_path)
                
                true_tokens = [item['token']
                               for item in title_sents[0]['features']]
                
                if is_consistent_prediction(pred_tokens, true_tokens):
                    stat = eval_stat(pred_tokens, true_tokens,
                                     accepted_labels)
                    if print_errors:
                        print_label_error(true_tokens,
                                          # we don't have features here
                                          features=None,
                                          instance_id=id_,
                                          excluded_indices=set([0]),
                                          correct_labels=map(get_label,
                                                             true_tokens),
                                          predicted_labels=map(get_label,
                                                               pred_tokens),
                                          target_true_label='IC',
                                          target_pred_label='AL',
                                          print_features=False)
                    ret_stat += stat
                    n_errorless += 1
                else:
                    logger.debug(
                        'Predicted and true tokens inconsisent:\n{}\n{}\n'.format(
                            pred_tokens, true_tokens)
                    )
            except:
                logger.error(traceback.format_exc())
                continue
            finally:
                n_finished += 1

    return ret_stat


if __name__ == "__main__":
    # from baseline1 import normalize_title as b1
    # from baseline2 import normalize_title as b2
    # from baseline3 import normalize_title as b3
    # evaluate(predicate_func = b2, pass_doc = True)
    # evaluate(predicate_func = b1)
    # evaluate(predicate_func=b3, 
    #          title_transformation_func=make_capitalized_title,
    #          pass_doc=True)
    r = eval_rule_based(
        output_path='/cs/taatto/home/hxiao/capitalization-recovery/result/puls-100k/rule-based/predictions-2015-09-07.txt',
        okform_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format',
        accepted_labels=set(['AL', 'IC']),
        print_errors=False)
    print(r)

