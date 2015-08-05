import json
import codecs
from pathlib import Path


def main(fname_paths):
    with codecs.open(fname_paths, 'r', 'utf8') as f:
        for l in f:
            fname, _ = json.loads(l.strip())
            print Path(fname).name


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
