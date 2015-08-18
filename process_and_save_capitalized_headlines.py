from pathlib import Path
from puls_util import extract_and_capitalize_headlines_from_corpus

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def process_and_save(corpus_dir, target_dir, docids):
    target_dir = Path(target_dir)
    headlines = extract_and_capitalize_headlines_from_corpus(corpus_dir,
                                                             docids)
    for i, (e, res) in enumerate(headlines):
        if e:
            logging.error(e)
        else:
            (docid, headlines) = res
            if i % 100 == 0:
                logging.info("{} / {} done".format(i, len(docids)))
                    
            target_path = (target_dir / Path(docid))
                
            # only make the non-existing ones
            if not target_path.exists():
                with target_path.open(mode='w', encoding='utf8') as f:
                    for hl in headlines:
                        f.write(' '.join(hl) + '\n')

if __name__ == "__main__":
    import sys

    corpus_dir = sys.argv[2]
    target_dir = sys.argv[3]

    with Path(sys.argv[1]).open() as f:
        docids = set([l.strip() for l in f])

    process_and_save(corpus_dir, target_dir, docids)
