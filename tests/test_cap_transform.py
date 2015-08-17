from capitalization_train.cap_transform import make_capitalized_title

from nose.tools import assert_equal


def test_make_capitalized_title():
    assert_equal(make_capitalized_title(title_words=['PaaS']), ['PaaS'])
    assert_equal(make_capitalized_title(title_words=['1.5']), ['1.5'])
    assert_equal(make_capitalized_title(title_words=['I', '1.5-MBA']),
                 ['I', '1.5-MBA'])
    assert_equal(make_capitalized_title(title_words=['1.5', 'PaaS']),
                 ['1.5', 'PaaS'])
    assert_equal(make_capitalized_title(title_words=['and', 'I']),
                 ['And', 'I'])
    assert_equal(make_capitalized_title(title_words=['I', 'And']),
                 ['I', 'and'])

    assert_equal(make_capitalized_title(title_words=['I', 'China']),
                 ['I', 'China'])
    assert_equal(make_capitalized_title(title_words=['MP']),
                 ['MP'])
    assert_equal(make_capitalized_title('Chromecast iOS'),
                 ['Chromecast', 'iOS'])

    assert_equal(make_capitalized_title('iPhone'),
                 ['iPhone'])
    assert_equal(make_capitalized_title('REally'),
                 ['REally'])
    

    words = make_capitalized_title(title='Etihad Airways announces new structure with equity airlines')
    assert_equal(words,
                 ['Etihad', 'Airways', 'Announces', 'New',
                  'Structure', 'with', 'Equity', 'Airlines'])
        
    assert_equal(make_capitalized_title(title_words='for 18th year'.split()),
                 ['For', '18th', 'Year'])

    words = make_capitalized_title(
        title="This translation app helps professionals traveling in China and Japan"
    )
    assert_equal(words,
                 ['This', 'Translation', 'App', 'Helps',
                  'Professionals', 'Traveling', 'in',
                  'China', 'and', 'Japan'])


    words = make_capitalized_title(
        title="Russia to see surge of investments if sanctions lifted: VTB Bank Head"
    )
    assert_equal(words, ['Russia', 'to', 'See', 'Surge', 'of',
                         'Investments', 'if', 'Sanctions', 'Lifted', ':',
                         'VTB', 'Bank', 'Head'])

    words = make_capitalized_title(title = "CIS FMs hold summit in Belarus")
    assert_equal(words, ['CIS', 'FMs', 'Hold', 'Summit', 'in', 'Belarus'])
    



