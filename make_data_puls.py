import sys
import json
import traceback
from data import convert_to_trainable_format
from cap_transform import make_capitalized_title
from pathlib import Path
from toolz.dicttoolz import get_in
from toolz.functoolz import partial

from capitalization_restoration.feature_extractor import FeatureExtractor


def printable_train_data(auxil_dir,
                         paf_dir,
                         ids,
                         extractor, feature_names,
                         start, end=None,
                         title_transform_func=make_capitalized_title):
    """

    Adapted to PULS requirement:
    
    - auxil file is read to get the additional prepreocessed features

    Parameters
    ------------
    auxil_dir: string
        the directory where all the .auxil files reside
    paf_dir: string
        the directory where all the .paf files reside
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
    auxil_dir = Path(auxil_dir)

    get_tokens = partial(map, partial(get_in, ['token']))
    get_tags = partial(map, partial(get_in, ['pos']))

    for i, id_ in enumerate(ids):
        if i < start:
            continue
            
        if i % 1000 == 0:
            sys.stderr.write("Finished %d\n" % i)

        if end is not None and i >= end:
            sys.stderr.write("Reached %d.\nTerminate.\n" % end)
            break

        try:
            with (auxil_dir / Path(id_)).with_suffix('.auxil')\
                                     .open(encoding='utf8') as f:
                # to get the last line
                for l in f:
                    pass

                docpath = str(paf_dir / Path(id_))

                try:
                    data = json.loads(l.strip())
                except ValueError:
                    sys.stderr.write('JSON parse error: {}\n'.format(l))
                    sys.stderr.write(traceback.format_exc())
                    continue

                try:
                    for sent in data['sents']:
                        title_tokens = get_tokens(sent['features'])
                        tags = get_tags(sent['features'])
                        words = convert_to_trainable_format(
                            title_tokens,
                            title_transform_func,
                            extractor,
                            docpath=docpath,
                            pos=tags
                        )
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
                    
                yield res
        except IOError:
            sys.stderr.write('IOError: {}/{}.auxil\n'.format(
                str(auxil_dir), id_)
            )
            sys.stderr.write(traceback.format_exc())

            continue
            

if __name__ == '__main__':
    with open('data/doc_ids_2015_08_05.txt', 'r') as f:
        ids = map(lambda s: s.strip(), f.readlines())

    auxil_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized/'
    paf_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format/'
    extractor = FeatureExtractor()
    start = int(sys.argv[1])
    
    try:
        end = int(sys.argv[2])
    except IndexError:
        end = None

    for l in printable_train_data(auxil_dir,
                                  paf_dir,
                                  ids,
                                  extractor=extractor,
                                  feature_names=extractor.feature_names,
                                  start=start, end=end,
                                  title_transform_func=make_capitalized_title):
        print l.encode('utf8')
