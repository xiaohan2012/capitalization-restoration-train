import os

from nose.tools import assert_equal

from capitalization_train.rule_based import output_labels


CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_output_labels():
    doc_ids = [
        '001BBB8BFFE6841FA498FCE88C43B63A',
        'existing'  # make sure it won't be processed
    ]
    mal_dir = CURDIR + '/data/docs_malformed'
    ok_dir = CURDIR + '/data/docs_okformed'

    label_path = CURDIR + '/data/docs_malformed/{}.labels'.format(doc_ids[0])
    if os.path.exists(label_path):
        os.remove(label_path)

    output_labels(doc_ids, ok_dir, mal_dir)
    
    # Nanobiotix Gets Early Positive Safety Results in Head and Neck Clinical Trial
    # Nanobiotix gets early Positive Safety rEsults IN head and neck clinical trial
    expected = ['IC', 'AL', 'AL', 'IC', 'IC', 'MX', 'AU',
                'AL', 'AL', 'AL', 'AL', 'AL']

    with open(label_path) as f:
        ls = f.readlines()
        assert_equal(1, len(ls))
        assert_equal(ls[0].split(), expected)

    with open(CURDIR + '/data/docs_malformed/{}.labels'.format(doc_ids[1])) as f:
        assert_equal(f.read(), 'I think therefore I exist')
        
