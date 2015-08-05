from puls_util import get_title_from_puls_core_output
from nose.tools import assert_equal


def test_multiple_titles():
    rawpath = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/4271571E96D5C726ECFDDDAACA74A264'
    titles = get_title_from_puls_core_output(rawpath + ".auxil",
                                             rawpath + ".paf",
                                             rawpath)

    assert_equal(len(titles), 2)


def test_single_title():
    rawpath = '/cs/fs/home/hxiao/code/capitalization_train/test_data/puls_format_raw/001BBB8BFFE6841FA498FCE88C43B63A'
    titles = get_title_from_puls_core_output(rawpath + ".auxil",
                                             rawpath + ".paf",
                                             rawpath)

    assert_equal(len(titles), 1)
