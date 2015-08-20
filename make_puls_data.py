import json
import time
import traceback
from pathlib import Path
from toolz.dicttoolz import get_in
from toolz.functoolz import (partial, compose)

from capitalization_restoration.feature_extractor import FeatureExtractor
from puls_util import separate_title_from_body
from data import convert_to_trainable_format
from cap_transform import make_capitalized_title

from errors import TitleInconsistencyError

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


value_mapping = {True: '--T',
                 False: '--F'}


def map_value_string(value):
    return value_mapping.get(value, value)


def printable_train_data(malform_data_dir,
                         okform_data_dir,
                         ids,
                         extractor, feature_names,
                         start, end=None,
                         title_transform_func=make_capitalized_title):
    """

    Adapted to PULS requirement:
    
    - auxil file is read to get the additional prepreocessed features

    Parameters
    ------------
    malform_data_dir: string
        the directory where the malformed data reside
    okform_data_dir: string
        the directory where the correctly formed data reside
    ids: list of string
        document ids
    extractor: FeatureExtractor
        the feature extractor
    feature_names: list of string
        the feature names
    start, end: int
        how many titles to extract
    title_transform_func: function
        funtion that accepts the title and transforms it
        into some badly capitalized version
    
    Returns
    ------------
    Generator of str:
        each str is one sentence, each line in the str is one token in the sent
        
    """
    feature_names += ['y']  # add the label feature name
    malform_data_dir = Path(malform_data_dir)

    # take care of this ["tickerSymbol",["NYSE","SKT"]]
    # /cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized/3987E0BD03749C996A04B881079AD753.auxil
    clean_tag = (lambda t: t[0] if isinstance(t, list) else t)
    get_tokens = partial(map, partial(get_in, ['token']))
    get_tags = partial(map, compose(clean_tag,
                                    partial(get_in, ['pos'])))
    get_lemmas = partial(map, partial(get_in, ['lemma']))

    n_collected = 0

    for i, id_ in enumerate(ids):
        if i < start:
            continue
            
        if i % 1000 == 0:
            logger.error("Collected %d" % n_collected)
            logger.error("Finished %d" % i)

        if end is not None and i >= end:
            logger.error("Reached %d. Terminate." % end)
            break

        try:
            with (malform_data_dir / Path(id_)).with_suffix('.auxil')\
                                               .open(encoding='utf8') as f:
                # to get the last line
                for l in f:
                    pass

                try:
                    data = json.loads(l.strip())
                except ValueError:
                    logger.debug('JSON parse error')
                    continue
                    
                okform_auxil_path = str((okform_data_dir /
                                         Path(id_)).with_suffix('.auxil'))
                okform_paf_path = str((okform_data_dir /
                                       Path(id_)).with_suffix('.paf'))
                try:
                    ok_title_sents, body_sents = separate_title_from_body(
                        okform_auxil_path,
                        okform_paf_path
                    )
                except (TypeError, IOError, ValueError):
                    logger.debug(traceback.format_exc())
                    continue

                # extract the tokens
                doc = [[t['token'] for t in sent['features']]
                       for sent in body_sents]

                ok_title_sents = list(ok_title_sents)

                bad_title_sents = data['sents']
                if not isinstance(bad_title_sents, list):
                    logger.debug('title sents not a list')
                    continue

                # we only consider headline that contains only ONE sentence
                if (len(ok_title_sents) ==  1 and
                    len(bad_title_sents) == 1):
                    for good_sent, bad_sent in zip(ok_title_sents,
                                                   bad_title_sents):
                        try:
                            good_title_tokens = get_tokens(good_sent['features'])
                            bad_title_tokens = get_tokens(bad_sent['features'])

                            # some validity checking
                            if len(good_title_tokens) != len(bad_title_tokens):
                                raise TitleInconsistencyError

                            if (map(lambda s: s.lower(), good_title_tokens) !=
                                map(lambda s: s.lower(), bad_title_tokens)):
                                    raise TitleInconsistencyError

                            tags = get_tags(bad_sent['features'])
                            lemmas = get_lemmas(bad_sent['features'])

                            # tag validity checking
                            for tag in tags:
                                if not (tag is None or
                                        isinstance(tag, basestring)):
                                    raise ValueError(
                                        '{}: tag {} not string'.format(id_, tag)
                                    )

                            # get malformed title tokens
                            words = convert_to_trainable_format(
                                good_title_tokens,
                                title_transform_func,
                                extractor,
                                doc=doc,
                                pos=tags,
                                lemma=lemmas
                            )
                        except TitleInconsistencyError:
                            logger.debug('TitleInconsistencyError')
                            continue
                        except:
                            logger.debug(traceback.format_exc())
                            continue

                    # format the features in the required form
                    res = unicode()
                    for word in words:
                        word_feature_str = u'\t'.join(
                            [unicode(map_value_string(word[feature_name]))
                             for feature_name in feature_names])
                        res += word_feature_str + '\n'
                    n_collected += 1
                    yield id_, res
        except IOError:
            logger.debug("{}.auxil file not found".format(id_))
            continue
            

if __name__ == '__main__':
    import sys
    from puls_util import get_doc_ids_from_file
    ids = get_doc_ids_from_file(sys.argv[1])

    malform_data_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized/'
    okform_data_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format/'
    extractor = FeatureExtractor()
    start = int(sys.argv[2])
    
    try:
        end = int(sys.argv[3])
    except IndexError:
        end = None

    successful_ids = []
    for id_, l in printable_train_data(malform_data_dir,
                                  okform_data_dir,
                                  ids,
                                  extractor=extractor,
                                  feature_names=extractor.feature_names,
                                  start=start, end=end,
                                  title_transform_func=make_capitalized_title):
        successful_ids.append(id_)
        print l.encode('utf8')

    with open('data/tmp/{}/trainable_doc_ids.txt'.format(
            time.strftime("%Y-%m-%d")),
            'w') as f:
        for i in successful_ids:
            f.write("{}\n".format(i))


