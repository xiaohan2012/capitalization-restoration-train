import os
from pathlib import Path
from capitalization_train.copy_puls_file_to_local import copy

from nose.tools import assert_equal

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_copy():
    local_dir = CURDIR + '/data/local_dir'
    # create one file first

    exist_names = ['/86FD993DE4DB76B74503D068A72A72BB',
                   '/86FD993DE4DB76B74503D068A72A72BB.paf']
    for name in exist_names:
        with open(local_dir + name, 'w') as f:
            f.write('I think therefore I exist')

    assert_equal(len(list(Path(local_dir).iterdir())), 2)

    copy(CURDIR + '/data/fnames_and_titles.txt',
         local_dir)
    
    assert_equal(len(list(Path(local_dir).iterdir())), 6)

    for name in exist_names:
        with open(local_dir + name, 'r') as f:
            assert_equal(f.read(), 'I think therefore I exist')
        
    for p in Path(local_dir).iterdir():
        p.unlink()
