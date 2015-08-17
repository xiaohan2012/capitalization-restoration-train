from word_shape_util import (without_alpha,
                             contains_lowercase,
                             contains_uppercase)


def get_label(word, **kwargs):
    """
    Possible labels
    
    IC: initial capital, note, there should be at least one alphabetic letter, and the alphabetic ones are in lower case 
    AU: all uppercase
    AL: all lowercase
    MX: mixed case
    AN: all no case
    """
    if without_alpha(word):
        return "AN"
    else:
        if word[0].isalpha():  # starts with alpha
            # a word
            if word.lower() == word:
                return "AL"
            elif (word[0].upper() == word[0] and
                  contains_lowercase(word) and
                  word[1:].lower() == word[1:]):
                return "IC"
            elif word.upper() == word:
                return "AU"
            else:
                return "MX"
        else:
            lower_flag = contains_lowercase(word)
            upper_flag = contains_uppercase(word)
            if lower_flag and upper_flag:
                return "MX"
            elif lower_flag and not upper_flag:
                return "AL"
            else:
                return "AU"
