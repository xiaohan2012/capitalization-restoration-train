import json
import codecs
import traceback

from pathlib import Path

from toolz.dicttoolz import get_in
from toolz.functoolz import compose
from toolz import (partial, map)

from util import get_title_position
from cap_transform import make_capitalized_title


def separate_title_from_body(aux_file_path,
                             paf_file_path):
    """
    """
    with codecs.open(aux_file_path, 'r', 'utf8') as aux_f:
        start, end = get_title_position(paf_file_path)
        data = json.loads(aux_f.read())

        within_range = (lambda sent:
                        sent['start'] >= start and sent['end'] <= end)

        title_sents = []
        body_sents = []
        for sent in data['sents']:
            if within_range(sent):
                title_sents.append(sent)
            else:
                body_sents.append(sent)
        return title_sents, body_sents


def extract_and_capitalize_headlines_from_corpus(corpus_dir, docids):
    """
    Iterate through all the files in `corpus_dir`,
    extract the headlines, capitalized and return them
    
    Parameter:
    ---------------
    corpus_dir: string

    docids: list of string
        the document to be processed

    Return:
    --------------
    generator of (docid, headlines): (str, list<list<str>>)
    """
    get_tokens = partial(map, partial(get_in, ['token']))
    get_features = partial(get_in, ['features'])
    
    make_capitalized_title_new = (lambda words:
                                  make_capitalized_title(title_words=words))
    
    for docid in docids:
        p = Path(corpus_dir) / Path(docid)
        auxil_p = p.with_suffix('.auxil')
        paf_p = p.with_suffix('.paf')
        if auxil_p.exists() and paf_p.exists():
            try:
                titles, _ = separate_title_from_body(
                    str(auxil_p),
                    str(paf_p))
            except:  # some .auxil is empty
                print "DOCID: {}".format(p)
                print(traceback.format_exc())

            # pipeline:
            # -> get features
            # -> get tokens
            # -> capitalize headline
            yield (p.name,
                   list(map(compose(make_capitalized_title_new,
                                    get_tokens, get_features),
                            titles)))


def get_doc_ids_from_file(path):
    """path: line based doc id file"""
    with open(path) as f:
        docids = set([l.strip() for l in f])
    return docids


def get_input_example(okform_dir, malformed_dir, id_):
    cap_title_path = str(Path(malformed_dir) / Path(id_)) + '.auxil'
    doc_path = str(Path(okform_dir) / Path(id_))
    
    _, docs = separate_title_from_body(doc_path + '.auxil',
                                       doc_path + '.paf')
    
    with codecs.open(cap_title_path, 'r', 'utf8') as f:
        title = json.loads(f.read())

    return {'capitalizedSentences': [title],
            'otherSentences': docs}
