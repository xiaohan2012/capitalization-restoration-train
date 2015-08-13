import os

from nose.tools import assert_equal

from capitalization_train.make_data_puls import printable_train_data
from capitalization_train.data import make_capitalized_title

from capitalization_restoration.feature_extractor import (FeatureExtractor,
                                                          LemmaFeature,
                                                          POSFeature)


CURDIR = os.path.dirname(os.path.realpath(__file__))

extractor = FeatureExtractor([LemmaFeature(), POSFeature()])


sent1_json = [{u'lemma': u'nanobiotix',
               u'pos': u'name_oov',
               u'token': u'Nanobiotix'},
              {u'lemma': u'get', u'pos': u'tv', u'token': u'gets'},
              {u'lemma': u'early', u'pos': u'd', u'token': u'early'},
              {u'lemma': u'positive', u'pos': u'adj', u'token': u'Positive'},
              {u'lemma': u'safety', u'pos': u'n', u'token': u'Safety'},
              {u'lemma': u'result', u'pos': u'n', u'token': u'rEsults'},
              {u'lemma': u'in', u'pos': u'csn', u'token': u'IN'},
              {u'lemma': u'head', u'pos': u'n', u'token': u'head'},
              {u'lemma': u'', u'pos': None, u'token': u'and'},
              {u'lemma': u'neck', u'pos': u'n', u'token': u'neck'},
              {u'lemma': u'clinical', u'pos': u'adj', u'token': u'clinical'},
              {u'lemma': u'trial', u'pos': u'n', u'token': u'trial'}]


malform_data_dir = CURDIR + '/data/docs_malformed/'
okform_data_dir = CURDIR + '/data/docs_okformed/'


def test_print_trainable_data():
    ids = ['001BBB8BFFE6841FA498FCE88C43B63A',
           '4B4DE4C180DB7697035273DB90BF5101']
    res = printable_train_data(malform_data_dir=malform_data_dir,
                               okform_data_dir=okform_data_dir,
                               ids=ids,
                               extractor=extractor,
                               feature_names=extractor.feature_names,
                               start=0, end=2,
                               title_transform_func=make_capitalized_title)
    sent1 = res.next()

    expected1 = """nanobiotix name_oov IC
get tv AL
early d AL
positive adj IC
safety n IC
result n MX
in csn AU
head n AL
and None AL
neck n AL
clinical adj AL
trial n AL
"""
    assert_equal(sent1, expected1)

    assert_equal(len(list(res)), 1)  # 2 sentences in total


