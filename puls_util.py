import json
import codecs

from pathlib import Path

from toolz.dicttoolz import get_in
from toolz.functoolz import compose
from toolz import (partial, map)

from util import get_title_position
from cap_transform import make_capitalized_title


def separate_title_from_body(aux_file_path,
                             paf_file_path):
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
            except Exception as e:
                yield (e, None)
            # pipeline:
            # -> get features
            # -> get tokens
            # -> capitalize headline
            yield (None, (p.name,
                          list(map(compose(make_capitalized_title_new,
                                           get_tokens, get_features),
                                   titles))))


def get_doc_ids_from_file(path):
    """path: line based doc id file"""
    with open(path) as f:
        docids = set([l.strip() for l in f])
    return docids


def convert_sentence_auxil_to_request(sent_auxil):
    assert isinstance(sent_auxil, dict), sent_auxil
    ret = {'no': sent_auxil['sentno']}
    ret['tokens'] = list(map(lambda r: r['token'], sent_auxil['features']))
    ret['pos'] = list(map(lambda r: r['pos'], sent_auxil['features']))
    return ret


def get_input_example(okform_dir, malformed_dir, id_):
    cap_title_path = str(Path(malformed_dir) / Path(id_)) + '.auxil'
    doc_path = str(Path(okform_dir) / Path(id_))
    
    _, docs = separate_title_from_body(doc_path + '.auxil',
                                       doc_path + '.paf')

    with codecs.open(cap_title_path, 'r', 'utf8') as f:
        for l in f:
            pass

        titles = list(map(
            convert_sentence_auxil_to_request,
            json.loads(l)['sents'])
        )
        
    doc_sents = list(map(
        convert_sentence_auxil_to_request,
        docs)
    )
    return {'capitalizedSentences': titles,
            'otherSentences': doc_sents
    }


if __name__ == '__main__':
    import sys
    import json
    ok_corpus_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
    malformed_corpus_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'
    res = get_input_example(ok_corpus_dir, malformed_corpus_dir, sys.argv[1])
    print(json.dumps(res).encode('utf8'))
