import codecs
import json
import shutil
from pathlib import Path


def main(fname_and_tile_file_path, target_dir):
    target_dir = Path(target_dir)
    if not target_dir.exists():
        target_dir.mkdir()

    with codecs.open(fname_and_tile_file_path, 'r', 'utf8') as global_f:
        for l in global_f:
            path, title = json.loads(l.strip())
            
            shutil.copy(path,
                        str(target_dir / Path(path).name))
            
            shutil.copy(path + '.paf',
                        str(target_dir / Path(Path(path).name + '.paf')))

if __name__ == "__main__":
    import sys
    src_path = sys.argv[1]
    target_dir = sys.argv[2]

    main(src_path, target_dir)
