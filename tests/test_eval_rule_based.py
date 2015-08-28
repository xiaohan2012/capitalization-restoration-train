import numpy as np
from numpy.testing import assert_array_equal
import os
from capitalization_train.evaluate import (eval_rule_based,
                                           is_consistent_prediction,
                                           eval_stat)
from nose.tools import (assert_equal,
                        assert_false,
                        assert_true)

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_eval_rule_based():
    actual = eval_rule_based(CURDIR + '/data/rule_based_output.txt',
                             okform_dir=CURDIR + '/data/docs_okformed/',
                             accepted_labels=['AL', 'IC'])
    expected = np.asarray([[10, 11, 10],
                           [5, 5, 6]])
    assert_array_equal(actual, expected)


def test_eval_stat():
    pred_tokens = ["SuperGroup", "sales", "rebound", "over", "Christmas",
                   "to", "defy", "city", "EXPECTATIONS"]
    true_tokens = 'SuperGroup sales rebound over Christmas to defy City EXPECTATIONS'.split()
    actual = eval_stat(pred_tokens, true_tokens, accepted_labels=['AL', 'IC'])
    expected = np.asarray([[5, 6, 5],
                           [1, 1, 2]])
    assert_array_equal(actual, expected)
    

def test_is_consistent_prediction():
    assert_false(
        is_consistent_prediction(['A'], ['A', 'extra token'])
    )

    assert_false(
        is_consistent_prediction(['A', 'B'], ['A', 'different'])
    )
    
    assert_true(
        is_consistent_prediction(['A', 'B'], ['A', 'B'])
    )
