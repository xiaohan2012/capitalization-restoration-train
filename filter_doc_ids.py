import os
from util import is_monocase
from puls_util import (get_doc_ids_from_file,
                       separate_title_from_body)


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(docids, directory):
    good_cnt = 0
    for i, id_ in enumerate(docids):
        if i % 1000 == 0:
            logger.info('{}/{}/{}'.format(good_cnt, i, len(docids)))

        path = os.path.join(directory, id_)
        titles, _ = separate_title_from_body(path + '.auxil', path + '.paf')
        tokens = [t['token']
                  for t in titles[0]['features']]
        if not is_monocase(tokens):
            print(id_)
            good_cnt += 1
        
if __name__ == '__main__':
    main(get_doc_ids_from_file('data/tmp/2015-08-18/trainable_doc_ids.txt'),
         '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format')
