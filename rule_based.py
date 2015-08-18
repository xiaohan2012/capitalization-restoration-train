import sys
from pathlib import Path
from puls_util import (separate_title_from_body, get_doc_ids_from_file)
from label import get_label

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def output_labels(doc_ids, good_corpus_dir, bad_corpus_dir):
    """
    Output the correct labels of the given documents specified in doc_ids
    under bad_corpus_dir
    """
    for i, doc_id in enumerate(doc_ids):
        if i % 1000 == 0:
            logger.info("{} / {}".format(i, len(doc_ids)))

        label_path = bad_corpus_dir + '/{}.labels'.format(doc_id)

        # skip if there
        if Path(label_path).exists():
            continue

        titles, _ = separate_title_from_body(
            good_corpus_dir + '/{}.auxil'.format(doc_id),
            good_corpus_dir + '/{}.paf'.format(doc_id)
        )
        
        assert len(titles) == 1, (titles, doc_id)
        good_title = titles[0]
        labels = [get_label(w['token']) for w in good_title['features']]

        with open(label_path, 'w') as f:
            f.write(' '.join(labels))
        

if __name__ == "__main__":
    output_labels(get_doc_ids_from_file(sys.argv[1]),
                  sys.argv[2],
                  sys.argv[3])
