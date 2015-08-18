import os
from nose.tools import assert_equal
from capitalization_train.process_and_save_capitalized_headlines import process_and_save
from pathlib import Path

CURDIR = os.path.dirname(os.path.realpath(__file__))
target_dir = CURDIR + '/data/puls-format-raw-capitalized/'


def test_process_and_save():
    # remove files first
    # while keeping one as 'already processed'
    fixed_doc_id = 'FB8778AEF476868557DDDDF98EF9D536'
    for p in Path(CURDIR + '/data/puls-format-raw-capitalized').iterdir():
        if p.name != fixed_doc_id:
            p.unlink()

    docids = [fixed_doc_id,
              '4271571E96D5C726ECFDDDAACA74A264']
    process_and_save(corpus_dir=CURDIR + '/../test_data/puls_format_raw',
                     target_dir=target_dir,
                     docids=docids)
    count = 0
    for p in Path(target_dir).iterdir():
        if p.suffix == '':
            count += 1
    
    assert_equal(count, len(docids))

    file_path = (target_dir +
                 '4271571E96D5C726ECFDDDAACA74A264')
    with Path(file_path).open(encoding='utf8') as f:
        assert_equal(f.read(),
                     'Public Internet Is Supposed to Lower Prices .\n' +
                     'In Seattle , It Could Work Too Well .\n')

    # check the unchanged one
    file_path = (target_dir +
                 'FB8778AEF476868557DDDDF98EF9D536')
    with Path(file_path).open(encoding='utf8') as f:
        assert_equal(f.read(), 'I am fake')
