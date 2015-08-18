import os
from nose.tools import assert_equal, assert_true
from capitalization_train.util import (extract_title,
                                       get_document_content_paf,
                                       is_monocase)


CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_extract_title():
    actual = extract_title(CURDIR + '/data/docs_okformed/001BBB8BFFE6841FA498FCE88C43B63A')
    expected = u'UPDATE - Nanobiotix gets early Positive Safety rEsults IN head and neck clinical trial'
    assert_equal(actual, expected)


def test_get_document_content_paf_empty():
    actual = get_document_content_paf(CURDIR + '/data/empty_doc')
    expected = '\n\n'
    assert_equal(actual, expected)


def test_get_document_content_paf():
    actual = get_document_content_paf(CURDIR + '/data/docs_okformed/001BBB8BFFE6841FA498FCE88C43B63A')
    assert_true(len(actual.strip()) > 400)


def test_is_monocase():
    assert_true(
        is_monocase(
            "The Inside Story of How the iPhone Crippled BlackBerry".split()
        )
    )
    
    # this
    assert_true(
        is_monocase(
            "Ayla Networks Executives Speaking at Key IoT Conferences this Spring".split()
        )
    )
    
    # annoying 'du'
    assert_true(
        is_monocase(
            "KSL Capital Partners Announces the Sale of Malmaison and Hotel du Vin".split()
        )
    )
