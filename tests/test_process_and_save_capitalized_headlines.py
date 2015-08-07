import os
from nose.tools import assert_equal
from capitalization_train.process_and_save_capitalized_headlines import process_and_save
from pathlib import Path

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_process_and_save():
    # remove files first
    for p in Path(CURDIR + '/data/puls-format-raw-capitalized').iterdir():
        p.unlink()

    process_and_save(corpus_dir=CURDIR + '/../test_data/puls_format_raw',
                     target_dir=CURDIR + '/data/puls-format-raw-capitalized')
    count = 0
    for p in Path(CURDIR + '/data/puls-format-raw-capitalized').iterdir():
        if p.suffix == '':
            count += 1
    
    assert_equal(count, 100)

    file_path = (CURDIR +
                 '/data/puls-format-raw-capitalized/' +
                 '4271571E96D5C726ECFDDDAACA74A264')
    with Path(file_path).open(encoding='utf8') as f:
        assert_equal(len(f.readlines()), 2)
