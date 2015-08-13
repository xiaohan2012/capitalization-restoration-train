from pathlib import Path
from puls_util import extract_and_capitalize_headlines_from_corpus


def process_and_save(corpus_dir, target_dir):
    target_dir = Path(target_dir)
    for i, (docid, headlines) in \
        enumerate(extract_and_capitalize_headlines_from_corpus(corpus_dir)):
        if i % 5000 == 0:
            print "{} done".format(i)
        with (target_dir / Path(docid)).open(mode='w', encoding='utf8') as f:
            for hl in headlines:
                f.write(' '.join(hl) + '\n')


if __name__ == "__main__":
    target_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'
    corpus_dir = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
    process_and_save(corpus_dir, target_dir)
