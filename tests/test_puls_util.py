from capitalization_train.puls_util import (get_title_from_puls_core_output,
                                            extract_and_capitalize_headlines_from_corpus)
from nose.tools import assert_equal


def test_multiple_titles():
    rawpath = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/4271571E96D5C726ECFDDDAACA74A264'
    titles = get_title_from_puls_core_output(rawpath + ".auxil",
                                             rawpath + ".paf",
                                             rawpath)

    assert_equal(len(list(titles)), 2)


def test_single_title():
    rawpath = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/001BBB8BFFE6841FA498FCE88C43B63A'
    titles = get_title_from_puls_core_output(rawpath + ".auxil",
                                             rawpath + ".paf",
                                             rawpath)

    assert_equal(len(list(titles)), 1)


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
