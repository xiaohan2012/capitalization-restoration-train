import re

contain_alpha_regexp = re.compile(r'[a-zA-Z]')


def without_alpha(s):
    """
    check if the string contains alphabetic value or not

    >>> without_alpha('sadf')
    False
    >>> without_alpha('123f')
    False
    >>> without_alpha('213')
    True
    """
    return contain_alpha_regexp.search(s) is None

contain_lower_regexp = re.compile(r'[a-z]')


def contains_lowercase(s):
    """
    check if the string contains lowercase character or not

    >>> contains_lowercase('sadf')
    True
    >>> contains_lowercase('123U')
    False
    >>> contains_lowercase('asdD')
    True
    """
    return contain_lower_regexp.search(s) is not None


contain_upper_regexp = re.compile(r'[A-Z]')


def contains_uppercase(s):
    """
    check if the string contains uppercase character or not

    >>> contains_uppercase('sadU')
    True
    >>> contains_uppercase('123a')
    False
    >>> contains_uppercase('asdD')
    True
    """
    return contain_upper_regexp.search(s) is not None
