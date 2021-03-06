import json
import os
import codecs
from capitalization_train.puls_util import (separate_title_from_body,
                                            extract_and_capitalize_headlines_from_corpus,
                                            get_input_example,
                                            get_doc_ids_from_file,
                                            convert_sentence_auxil_to_request)
from nose.tools import assert_equal


CURDIR = os.path.dirname(os.path.realpath(__file__))


with codecs.open(CURDIR + '/data/001BBB8BFFE6841FA498FCE88C43B63A.title.json') as f:
    title_sent = json.loads(f.read())

with codecs.open(CURDIR + '/data/001BBB8BFFE6841FA498FCE88C43B63A.title-cap.json') as f:
    cap_title_sent = json.loads(f.read())

with codecs.open(CURDIR + '/data/001BBB8BFFE6841FA498FCE88C43B63A.body.json') as f:
    body_sents = json.loads(f.read())


def test_separate_title_from_body():
    assert_equal.__self__.maxDiff = None
    rawpath = CURDIR + '/data/docs_okformed/001BBB8BFFE6841FA498FCE88C43B63A'
    title_sents, body_sents = separate_title_from_body(rawpath + ".auxil",
                                                       rawpath + ".paf")
    assert_equal(len(title_sents), 1)
    assert_equal(len(body_sents), 20)
    assert_equal(title_sents[0], title_sent)


def test_extract_and_capitalize_headlines_from_corpus():
    doc_ids = ['EEBADC60811702C931B0F6CB61CE9054',
               '4271571E96D5C726ECFDDDAACA74A264']
    corpus_dir = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/'
    result = list(extract_and_capitalize_headlines_from_corpus(
        corpus_dir, doc_ids)
    )
    print(result[0])
    assert_equal(len(result), 2)
    assert_equal(result[0][0], None)
    assert_equal(len(result[0][1][1]), 1)
    assert_equal(result[0][1][0], 'EEBADC60811702C931B0F6CB61CE9054')
    assert_equal(result[0][1][1],
                 [[u'Microsoft', u'Gives', u'New', u'Brand', u'Identity',
                  u'to', u'Nokia', u'Retail', u'Stores']])

    result1 = filter(lambda (_, (docid, __)):
                     docid == '4271571E96D5C726ECFDDDAACA74A264',
                     result)
    
    assert_equal(len(result1[0][1][1]), 2)


def test_input_example():
    actual = get_input_example(
        CURDIR + '/data/docs_okformed/',
        CURDIR + '/data/docs_malformed/',
        '001BBB8BFFE6841FA498FCE88C43B63A'
    )
    print(cap_title_sent)
    expected = {"capitalizedSentences":
                [convert_sentence_auxil_to_request(
                    cap_title_sent)],
                "otherSentences": map(
                    convert_sentence_auxil_to_request,
                    body_sents)
    }
    print(expected)
    assert_equal(actual, expected)


def test_convert_sentence_auxil_to_request():
    sent_auxil = {"sentno":0,"start":51,"end":128,"features":[{"lemma":"nanobiotix","pos":"name_oov","token":"Nanobiotix"},{"lemma":"get","pos":"tv","token":"Gets"},{"lemma":"early","pos":"d","token":"Early"},{"lemma":"positive","pos":"adj","token":"Positive"},{"lemma":"safety","pos":"n","token":"Safety"},{"lemma":"result","pos":"n","token":"Results"}]}
    actual = convert_sentence_auxil_to_request(sent_auxil)
    expected = {'no': 0,
                'tokens': ['Nanobiotix', 'Gets', 'Early', 'Positive', 'Safety', 'Results'],
                'pos': ['name_oov', 'tv', 'd', 'adj', 'n', 'n']
    }
    assert_equal(actual, expected)
    

def test_get_doc_ids_from_file():
    ids = get_doc_ids_from_file(CURDIR + '/data/docids.txt')
    assert_equal(len(ids), 4)
