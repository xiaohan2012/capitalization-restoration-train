import sys
import json
import traceback
from pathlib import Path
from toolz.dicttoolz import get_in
from toolz.functoolz import (partial, compose)

from capitalization_restoration.feature_extractor import FeatureExtractor
from puls_util import get_title_from_puls_core_output
from data import convert_to_trainable_format
from cap_transform import make_capitalized_title


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
    clean_lemma = (lambda t: '--EMPTY--' if len(t) == 0 else t)
    get_lemmas = partial(map, compose(clean_lemma,
                                      partial(get_in, ['lemma'])))

    n_collected = 0

    for i, id_ in enumerate(ids):
        if i < start:
            continue
            
        if i % 1000 == 0:
            sys.stderr.write("Collected %d\n" % n_collected)
            sys.stderr.write("Finished %d\n" % i)

        if end is not None and i >= end:
            sys.stderr.write("Reached %d.\nTerminate.\n" % end)
            break

        try:
            with (malform_data_dir / Path(id_)).with_suffix('.auxil')\
                                               .open(encoding='utf8') as f:
                # to get the last line
                for l in f:
                    pass

                docpath = str(okform_data_dir / Path(id_))

                try:
                    data = json.loads(l.strip())
                except ValueError:
                    sys.stderr.write('JSON parse error: {}\n'.format(l))
                    sys.stderr.write(traceback.format_exc())
                    continue
                    
                okform_auxil_path = str((okform_data_dir /
                                         Path(id_)).with_suffix('.auxil'))
                okform_paf_path = str((okform_data_dir /
                                       Path(id_)).with_suffix('.paf'))
                try:
                    normal_case_titles = get_title_from_puls_core_output(
                        okform_auxil_path,
                        okform_paf_path
                    )
                except (TypeError, IOError, ValueError):
                    sys.stderr.write(traceback.format_exc())
                    continue
                normal_case_titles = list(normal_case_titles)

                if not isinstance(data['sents'], list):
                    sys.stderr.write('No headline available\n')
                    continue

                # we only consider headline that contains only ONE sentence
                if not (len(normal_case_titles) == 1 and
                        len(data['sents']) == 1):
                    sys.stderr.write('Sentence segmentation inconsistent:\n')
                    sents_str = lambda sents: '\n'.join(
                        [' '.join(get_tokens(sent['features']))
                         for sent in sents]
                    )
                    sys.stderr.write('Good:\n' + sents_str(normal_case_titles))
                    sys.stderr.write('Bad:\n' + sents_str(data['sents']))
                    continue

                try:
                    good_sent, bad_sent\
                        = normal_case_titles[0], data['sents'][0]

                    good_title_tokens = get_tokens(good_sent['features'])
                    bad_title_tokens = get_tokens(bad_sent['features'])

                    # some validity checking
                    assert len(good_title_tokens) == len(bad_title_tokens)
                    for good_token, bad_token in zip(good_title_tokens,
                                                     bad_title_tokens):
                        assert good_token.lower() == bad_token.lower()

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
                        docpath=docpath,
                        pos=tags,
                        lemma=lemmas
                    )
                except AssertionError:
                    sys.stderr.write('Sentence content inconsistent:\n')
                    sys.stderr.write('Good:' + json.dumps(good_title_tokens)
                                     + '\n')
                    sys.stderr.write('Bad:' + json.dumps(bad_title_tokens)
                                     + '\n')
                    continue
                except:
                    sys.stderr.write(json.dumps(data) + '\n')
                    sys.stderr.write(traceback.format_exc())
                    continue

                # format the features in the required form
                res = unicode()
                for word in words:
                    word_feature_str = u' '.join(
                        [unicode(word[feature_name])
                         for feature_name in feature_names])
                    res += word_feature_str + '\n'
                n_collected += 1
                yield res
        except IOError:
            sys.stderr.write('IOError: {}/{}.auxil\n'.format(
                str(malform_data_dir), id_)
            )
            sys.stderr.write(traceback.format_exc())

            continue
            

if __name__ == '__main__':
    with open('data/doc_ids_2015_08_05.txt', 'r') as f:
        ids = map(lambda s: s.strip(), f.readlines())

    malform_data_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized/'
    okform_data_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format/'
    extractor = FeatureExtractor()
    start = int(sys.argv[1])
    
    try:
        end = int(sys.argv[2])
    except IndexError:
        end = None

    for l in printable_train_data(malform_data_dir,
                                  okform_data_dir,
                                  ids,
                                  extractor=extractor,
                                  feature_names=extractor.feature_names,
                                  start=start, end=end,
                                  title_transform_func=make_capitalized_title):
        print l.encode('utf8')
