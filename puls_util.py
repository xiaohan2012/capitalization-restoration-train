import json
import codecs
import traceback

from pathlib import Path

from toolz.dicttoolz import get_in
from toolz.functoolz import compose
from toolz import (partial, map, filter)

from util import get_title_position
from cap_transform import make_capitalized_title


def get_title_from_puls_core_output(aux_file_path,
                                    paf_file_path,
                                    main_file_path):
    """
    """
    with codecs.open(aux_file_path, 'r', 'utf8') as aux_f, \
         codecs.open(main_file_path, 'r', 'utf8') as main_f:
        start, end = get_title_position(paf_file_path)
        data = json.loads(aux_f.read())

        within_range = (lambda sent:
                        sent['start'] >= start and sent['end'] <= end)

        return filter(within_range, data['sents'])


def extract_and_capitalize_headlines_from_corpus(corpus_dir):
    """
    Iterate through all the files in `corpus_dir`,
    extract the headlines, capitalized and return them
    
    Parameter:
    ---------------
    corpus_dir: string

    Return:
    --------------
    generator of (docid, headlines): (str, list<list<str>>)
    """
    get_tokens = partial(map, partial(get_in, ['token']))
    get_features = partial(get_in, ['features'])
    
    make_capitalized_title_new = (lambda words:
                                  make_capitalized_title(title_words=words))

    for p in Path(corpus_dir).iterdir():
        if p.suffix == '':
            auxil_p = p.with_suffix('.auxil')
            paf_p = p.with_suffix('.paf')
            if auxil_p.exists() and paf_p.exists():
                try:
                    titles = get_title_from_puls_core_output(
                        str(auxil_p),
                        str(paf_p),
                        str(p))
                except ValueError:  # some .auxil is empty
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
