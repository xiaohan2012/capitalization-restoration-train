import nltk
from ground_truth import (ARTICLES, PREPOSITIONS, CONJUNCTIONS)

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
