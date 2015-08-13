import json
import os

from capitalization_train.puls_util import (separate_title_from_body,
                                            extract_and_capitalize_headlines_from_corpus)
from nose.tools import assert_equal


CURDIR = os.path.dirname(os.path.realpath(__file__))


title_sent = '{"sentno":0,"start":51,"end":128,"features":[{"lemma":"nanobiotix","pos":"name_oov","token":"Nanobiotix"},{"lemma":"get","pos":"tv","token":"gets"},{"lemma":"early","pos":"d","token":"early"},{"lemma":"positive","pos":"adj","token":"Positive"},{"lemma":"safety","pos":"n","token":"Safety"},{"lemma":"result","pos":"n","token":"rEsults"},{"lemma":"in","pos":"csn","token":"IN"},{"lemma":"head","pos":"n","token":"head"},{"lemma":"","pos":null,"token":"and"},{"lemma":"neck","pos":"n","token":"neck"},{"lemma":"clinical","pos":"adj","token":"clinical"},{"lemma":"trial","pos":"n","token":"trial"}]}'


def test_separate_title_from_body():
    rawpath = CURDIR + '/data/docs_okformed/001BBB8BFFE6841FA498FCE88C43B63A'
    title_sents, body_sents = separate_title_from_body(rawpath + ".auxil",
                                                       rawpath + ".paf")
    assert_equal(len(title_sents), 1)
    assert_equal(len(body_sents), 20)
    assert_equal(title_sents[0], json.loads(title_sent))


def test_extract_and_capitalize_headlines_from_corpus():
    corpus_dir = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/'
    result = list(extract_and_capitalize_headlines_from_corpus(corpus_dir))
    assert_equal(len(result), 100)
    assert_equal(result[0][0], 'EEBADC60811702C931B0F6CB61CE9054')
    assert_equal(len(result[0][1]), 1)
    assert_equal(result[0][1][0],
                 [u'Microsoft', u'Gives', u'New', u'Brand', u'Identity',
                  u'to', u'Nokia', u'Retail', u'Stores'])

    result1 = filter(lambda (docid, _):
                     docid == '4271571E96D5C726ECFDDDAACA74A264',
                     result)[0]
    
    assert_equal(len(result1[1]), 2)
