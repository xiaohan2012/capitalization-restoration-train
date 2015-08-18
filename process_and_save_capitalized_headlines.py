from pathlib import Path
from puls_util import extract_and_capitalize_headlines_from_corpus


def process_and_save(corpus_dir, target_dir, docids):
    target_dir = Path(target_dir)
    for i, (docid, headlines) in \
        enumerate(
            extract_and_capitalize_headlines_from_corpus(corpus_dir, docids)):
        print(docid)
        if i % 5000 == 0:
            print "{} / {} done".format(i, len(docids))
        target_path = (target_dir / Path(docid))
        
        # only make the non-existing ones
        if not target_path.exists():
            with target_path.open(mode='w', encoding='utf8') as f:
                for hl in headlines:
                    f.write(' '.join(hl) + '\n')


if __name__ == "__main__":
    import sys

    target_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'
    corpus_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'

    with Path(sys.argv[1]).open() as f:
        docids = set([l.strip() for l in f])

    process_and_save(corpus_dir, target_dir, docids)
