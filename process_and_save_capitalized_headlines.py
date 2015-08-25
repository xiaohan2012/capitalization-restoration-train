from pathlib import Path
from puls_util import extract_and_capitalize_headlines_from_corpus

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process_and_save(corpus_dir, target_dir, docids, refresh=False):
    target_dir = Path(target_dir)
    headlines = extract_and_capitalize_headlines_from_corpus(corpus_dir,
                                                             docids)

    for i, (e, res) in enumerate(headlines):
        if e:
            logger.error('Error:', e)
        else:
            (docid, headlines) = res
            if i % 100 == 0:
                logger.info("{} / {} done".format(i, len(docids)))
                    
            target_path = (target_dir / Path(docid))
            
            # only make the non-existing ones
            if refresh or not target_path.exists():
                logger.info("processed: {}".format(docid))
                with target_path.open(mode='w', encoding='utf8') as f:
                    for hl in headlines:
                        f.write(' '.join(hl) + '\n')

if __name__ == "__main__":
    import sys

    corpus_dir = sys.argv[2]
    target_dir = sys.argv[3]

    with Path(sys.argv[1]).open() as f:
        docids = set([l.strip() for l in f])

    process_and_save(corpus_dir, target_dir, docids, refresh=True)
