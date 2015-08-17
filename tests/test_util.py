import os
from nose.tools import assert_equal
from capitalization_train.util import extract_title


CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_extract_title():
    actual = extract_title(CURDIR + '/data/docs_okformed/001BBB8BFFE6841FA498FCE88C43B63A')
    expected = u'UPDATE - Nanobiotix gets early Positive Safety rEsults IN head and neck clinical trial'
    assert_equal(actual, expected)
