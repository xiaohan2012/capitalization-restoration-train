from capitalization_train.label import get_label

from nose.tools import assert_equal


def test_get_label():
    assert_equal(get_label(u'Click'), 'IC')
    assert_equal(get_label(u'Very-funny'), 'IC')
    assert_equal(get_label(u'Fb11'), 'IC')

    assert_equal(get_label(u'F11'), 'AU')
    assert_equal(get_label(u'B'), 'AU')
    assert_equal(get_label(u'OK'), 'AU')
    assert_equal(get_label(u'11.5A'), 'AU')
    
    assert_equal(get_label(u'lower'), 'AL')
    assert_equal(get_label(u'11.5a'), 'AL')
    assert_equal(get_label(u'f11'), 'AL')
    
    assert_equal(get_label(u'/hone/Doc'), 'MX')
    assert_equal(get_label(u'HealthCare'), 'MX')
    assert_equal(get_label(u'SaaS'), 'MX')
    assert_equal(get_label(u'healthCare'), 'MX')
    assert_equal(get_label(u'iPhone'), 'MX')
    assert_equal(get_label(u'11.5Aa'), 'MX')

    assert_equal(get_label(u'$123'), 'AN')
    assert_equal(get_label(u'.'), 'AN')
    assert_equal(get_label(u'.&%*%'), 'AN')

