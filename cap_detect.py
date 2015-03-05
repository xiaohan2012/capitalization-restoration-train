from ground_truth import (ARTICLES, PREPOSITIONS, CONJUNCTIONS)

def capitalized(title_words):
    """
    Determine if the title words are already capitalized

    >>> capitalized("Global Eagle Entertainment and SES Sign a Strategic Partnership to Deliver Global Ku-Band Satellite in-Flight Connectivity to Airlines".split())
    True
    >>> capitalized("Agenda Released for the 17th annual Summit on Superbugs & Superdrugs".split())
    False
    >>> capitalized("How Find Your Inner Martin Scorsese to Build Brand & Rule the World".split())
    True
    >>> capitalized("Half of YouTube's Traffic is Now Coming From Mobile: CEO".split()) # doctest: +SKIP
    True
    >>> capitalized("Crystal Bridges Announces 2015 Exhibits, Including Warhol, van Gogh, Pollock".split()) # doctest: +SKIP
    """
    for word in title_words[1:]:
        prefix = word.split("-")[0] #handle the in-Flight case
        should_be_lower = lambda w: (w in ARTICLES or
                                     w in PREPOSITIONS or
                                     w in CONJUNCTIONS)

        if should_be_lower(word) or should_be_lower(prefix):
            continue
        elif word[0].isalpha() and word[0].lower() == word[0]: # there is some lower cased words besides articles prepositions and conjunctions
            return False

    return True


def all_lowercase(title_words):
    """
    if the words are all in lowercase

    >>> all_lowercase(["a", "b", "c"])
    True
    >>> all_lowercase(["a", "12b", "c12"])
    True
    >>> all_lowercase(["a", "12b", "C12"])
    False
    """
    concat_str = ''.join(title_words)
    return concat_str.lower() == concat_str

def all_uppercase(title_words):
    """
    if the words are all in uppercase

    >>> all_uppercase(["A", "B", "C"])
    True
    >>> all_uppercase(["A", "12B", "C12"])
    True
    >>> all_uppercase(["A", "12B", "c12"])
    False
    """
    concat_str = ''.join(title_words)
    return concat_str.upper() == concat_str

