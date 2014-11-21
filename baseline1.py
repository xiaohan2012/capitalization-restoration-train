"""
Baseline capitalization restorer

It checks whether the word exists in dictionary or not
"""


import enchant
d = enchant.Dict("en_US")

def normalize_title(title = "", words = []):
    """
    >>> title = 'Cyan Holdings represented at heavyweight round-table event in India'
    >>> normalize_title(words = make_capitalized_title(title = title))
    ['Cyan', 'holdings', 'represented', 'at', 'heavyweight', 'round-table', 'event', 'in', 'India']
    """
    if title:
        words = nltk.word_tokenize(title)

    head = words[0][0].upper() + words[0][1:]
    tail = words[1:]
    return [head] + [(w
                      if d.check(w) and not d.check(w.lower()) #Only the upper case word is in the dictionary, for example `Google` is in while `google` is not
                      else
                      w[0].lower() + w[1:])
                     for w in tail]

if __name__  == "__main__":
    import doctest
    doctest.testmod()
