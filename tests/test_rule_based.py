import os

from nose.tools import assert_equal

from capitalization_train.rule_based import (output_labels,
                                             make_rule_based_corpus)

from pathlib import Path

CURDIR = os.path.dirname(os.path.realpath(__file__))

mal_dir = CURDIR + '/data/docs_malformed'
ok_dir = CURDIR + '/data/docs_okformed'
rb_dir = CURDIR + '/data/docs_rule_based'

def test_output_labels():
    doc_ids = [
        '001BBB8BFFE6841FA498FCE88C43B63A',
        'existing'  # make sure it won't be processed
    ]

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
        

def test_make_rule_based_corpus():
    ids = ['001BBB8BFFE6841FA498FCE88C43B63A',
           '4B4DE4C180DB7697035273DB90BF5101']
    
    for id_ in ids:
        p = Path(rb_dir, id_)
        if p.exists():
            p.unlink()

    make_rule_based_corpus(ids, ok_dir, rb_dir)
    
    cnt = 0
    for id_ in ids:
        p = Path(rb_dir, id_)
        if p.exists():
            cnt += 1
    assert_equal(cnt, len(ids))
        
    with Path(rb_dir, ids[0]).open('r', encoding='utf8') as f:
        lines = f.readlines()
        assert_equal('20150609\n', lines[0])
        assert_equal('001BBB8BFFE6841FA498FCE88C43B63A\n', lines[1])
        assert_equal(u'UPDATE - Nanobiotix Gets Early Positive Safety rEsults in Head and Neck Clinical Trial\n',
                     lines[2])
        assert_equal(len(lines), 19)        
