import nltk
from ground_truth import (ARTICLES, PREPOSITIONS, CONJUNCTIONS)
from operator import itemgetter

def make_capitalized_title(title = None, title_words = None):
    """
    >>> make_capitalized_title(title = "This translation app helps professionals traveling in China and Japan")
    ['This', 'Translation', 'App', 'Helps', 'Professionals', 'Traveling', 'in', 'China', 'and', 'Japan']
    >>> make_capitalized_title(title = "Russia to see surge of investments if sanctions lifted: VTB Bank Head")
    ['Russia', 'to', 'See', 'Surge', 'of', 'Investments', 'if', 'Sanctions', 'Lifted', ':', 'VTB', 'Bank', 'Head']
    >>> make_capitalized_title(title = "CIS FMs hold summit in Belarus")
    ['CIS', 'FMs', 'Hold', 'Summit', 'in', 'Belarus']
    """
    
    trans_words = []
    if title_words:
        words = title_words
    elif title:
        words = nltk.word_tokenize(title)
    else:
        raise ValueError("Receive nothing..")

    for i, word in enumerate(words):
        if i == 0:
            trans_words.append(word if word[0] == word[0].upper() else word.capitalize())
        elif (word in ARTICLES or word in PREPOSITIONS or word in CONJUNCTIONS):
            trans_words.append(word)
        elif word[0] == word[0].upper(): #already capitalized
            trans_words.append(word)
        else:
            trans_words.append(word.capitalize())
    return trans_words

def make_uppercase_title(title_words):
    """make the title uppercase

    >>> make_uppercase_title(["This", "translation", "app", "helps", "professionals", "traveling", "in", "China", "and", "Japan"])
    ['THIS', 'TRANSLATION', 'APP', 'HELPS', 'PROFESSIONALS', 'TRAVELING', 'IN', 'CHINA', 'AND', 'JAPAN']
    """
    words = []
    for w in title_words:
        words.append(w.upper())
        
    return words

def make_lowercase_title(title_words):
    """make the title lowercase

    >>> make_lowercase_title(["This", "translation", "app", "helps", "professionals", "traveling", "in", "China", "and", "Japan"])
    ['this', 'translation', 'app', 'helps', 'professionals', 'traveling', 'in', 'china', 'and', 'japan']
    """
    words = []
    for w in title_words:
        words.append(w.lower())
        
    return words


def transform_data(data, sent_transform_func):
    """
    Transform the data on the sentence level
    
    >>> input = [[(u'The', 'IC'), (u'Sun', 'IC'), (u'Life', 'IC'), (u'Building', 'IC'), (u'receives', 'AL'), (u'LEED', 'AU'), (u'Silver', 'IC'), (u'Certification', 'IC')]]
    >>> transform_data(input, make_capitalized_title)
    [[(u'The', 'IC'), (u'Sun', 'IC'), (u'Life', 'IC'), (u'Building', 'IC'), (u'Receives', 'AL'), (u'LEED', 'AU'), (u'Silver', 'IC'), (u'Certification', 'IC')]]
    >>> transform_data(input, make_lowercase_title)
    [[(u'the', 'IC'), (u'sun', 'IC'), (u'life', 'IC'), (u'building', 'IC'), (u'receives', 'AL'), (u'leed', 'AU'), (u'silver', 'IC'), (u'certification', 'IC')]]
    """
    assert callable(sent_transform_func)

    new_data = []
    for instance in data:
        new_data.append(
            zip(sent_transform_func(title_words = map(itemgetter(0), instance)), 
                map(itemgetter(1), instance))
        )
    return new_data
