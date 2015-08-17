# -*- coding: utf-8 -*-

import sys, re, json, string

import nltk
from codecs import open

from util import (get_file_names, 
                  extract_title, 
                  get_document_content_paf,
                  get_document_content)

from cap_transform import (make_capitalized_title,
                           make_lowercase_title,
                           make_uppercase_title)

from word_shape_util import (without_alpha, 
                             contains_lowercase, 
                             contains_uppercase)

from capitalization_restoration.feature_extractor import FeatureExtractor
    

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
        if word[0].isalpha(): # starts with alpha
            # a word
            if word.lower() == word:
                return "AL"
            elif word[0].upper() == word[0] and contains_lowercase(word) and word[1:].lower() == word[1:]:
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
                
    if word.upper() == word:
        return "AU"
    elif word[0].isalpha() and word[0] == word[0].upper():
        return "C"
    elif word[0].isalpha():
        return "L"
    else:
        return "I"
        # raise ValueError("Invalid value `%s`" %(word))


def convert_to_trainable_format(title, title_transform_func, feature_extractor, **kwargs):
    """
    Given some title(before capitalization), return the trainable(for CRF-suite) format
    
    >>> from cap_transform import make_capitalized_title
    >>> from capitalization_restoration.feature_extractor import FeatureExtractor
    >>> extractor = FeatureExtractor()
    >>> sent = convert_to_trainable_format(u"Why oil prices will be 'robust' long-term: Shell CEO", make_capitalized_title, extractor, docpath="test_data/oil-price")
    >>> sent[2]["word"]
    u'Prices'
    >>> sent[5]["lower-in-dict"]
    False
    >>> sent[1]["y"]
    'AL'
    """
    if isinstance(title, list):
        words = title
    else:
        words = nltk.word_tokenize(title)

    transformed_words = title_transform_func(title_words = words)

    words_with_features = feature_extractor.extract(transformed_words, **kwargs)

    #add the labels
    for word_str, word_info in zip(words, words_with_features):
        word_info["y"] = get_label(word_str)

    return words_with_features


def print_trainable_data(path,
                         extractor, feature_names,
                         start, end = None,
                         title_transform_func = make_capitalized_title):
    """
    >>> extractor = FeatureExtractor()
    >>> print_trainable_data(path = "test_data/mixed-case.info", extractor = extractor, feature_names = extractor.feature_names, start = 0, end = 1, title_transform_func = make_capitalized_title) #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    One True True True True True False True False CD False True IC
    ...
    PaaS False False False False False False True False NNP True False MX
    ...
    Heroku False False False False False False True False NNP False False IC
    ...
    IBM False False True False True True True False NNP True False AU
    ...
    """
    feature_names += ['y'] #add the label feature name

    # sys.stderr.write(" ".join(feature_names) + "\n")

    i = 0
    with open(path, "r", "utf8") as f:
        for line in f:
            fname, title = json.loads(line)
            if i < start:
                i += 1
                continue
            
            if i % 1000 == 0:
                sys.stderr.write("Finished %d\n" %i)
            
            words = convert_to_trainable_format(title,
                                                title_transform_func,
                                                extractor,
                                                docpath=fname
                                            )

            # print the features in the required format
            for word in words:
                word_feature_str = ' '.join([unicode(word[feature_name]) for feature_name in feature_names])
                print unicode(word_feature_str).encode('utf8')
            print 
            
            i += 1

            if end is not None and i >= end:
                sys.stderr.write("Reached %d.\nTerminate.\n" %(end))
                break


def load_labeled_data(path):
    """

    >>> d = load_labeled_data(path = "fnames_and_titles.txt")
    >>> d.next()[:8]
    [(u'The', 'IC'), (u'Sun', 'IC'), (u'Life', 'IC'), (u'Building', 'IC'), (u'receives', 'AL'), (u'LEED', 'AU'), (u'Silver', 'IC'), (u'Certification', 'IC')]
    """
    with open(path, "r", "utf8") as f:
        for line in f:
            _, title = json.loads(line)
            words = nltk.word_tokenize(title)
            yield [(w, get_label(w)) for w in words]

if __name__ == "__main__":
    import sys

    path = sys.argv[1]
    op = sys.argv[2]
    start = int(sys.argv[3])
    
    try:
        end = int(sys.argv[4])
    except IndexError:
        end = None
    
    op_table = {
        "upper": make_uppercase_title,
        "lower": make_lowercase_title,
        "cap": make_capitalized_title
    }
    assert op in op_table.keys()
    
    extractor = FeatureExtractor()
    
    print_trainable_data(path = sys.argv[1],
                         extractor = extractor,
                         feature_names = extractor.feature_names,
                         start = start, end = end,
                         # content_extractor = get_document_content,
                         title_transform_func = op_table[op])
    # path = "test-titles.txt",       
