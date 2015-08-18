import codecs
import json
import shutil
from pathlib import Path


def copy(fname_and_tile_file_path, target_dir):
    target_dir = Path(target_dir)
    if not target_dir.exists():
        target_dir.mkdir()

    with codecs.open(fname_and_tile_file_path, 'r', 'utf8') as global_f:
        for i, l in enumerate(global_f):
            if i % 100 == 0:
                print("{} finished".format(i))

            path, title = json.loads(l.strip())
            
            target_path_text = target_dir / Path(path).name
            if not target_path_text.exists():
                shutil.copy(path,
                            str(target_path_text))

            target_path_paf = (target_dir /
                               Path(Path(path).name).with_suffix('.paf'))
            if not target_path_paf.exists():
                shutil.copy(path + '.paf',
                            str(target_path_paf))

if __name__ == "__main__":
    import sys
    src_path = sys.argv[1]
    target_dir = sys.argv[2]

    copy(src_path, target_dir)
