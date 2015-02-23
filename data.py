# -*- coding: utf-8 -*-

import sys, re, json, string

import nltk
from codecs import open
from guess_language import guessLanguage

from util import (get_file_names, 
                  extract_title, 
                  make_capitalized_title,
                  make_lowercase_title,
                  make_uppercase_title, 
                  get_document_content_paf,
                  get_document_content, 
                  is_monocase, 
                  normalize_title)

from word_shape_util import (without_alpha, 
                             contains_lowercase, 
                             contains_uppercase)
from feature import *

from ground_truth import (articles, prepositions, conjunctions)

def print_filenames_and_titles():
    """print title each per one line from the corpus"""
    paths = ['/group/home/puls/Shared/capitalization-recovery/%2d' %i 
             for i in xrange(9, 32)]    
    titles = []
    for fname in get_file_names(paths):
        title = extract_title(fname)
        
        if not title: # no title
            continue
            
        title = normalize_title(title)
        
        if not is_monocase(nltk.word_tokenize(title)) and guessLanguage(title) == "en": #is not monocase and is English
            print json.dumps([fname, unicode(title).encode("utf8")])
    
def get_label(word, **kwargs):
    """
    Possible labels
    
    IC: initial capital, note, there should be at least one alphabetic letter, and the alphabetic ones are in lower case 
    AU: all uppercase
    AL: all lowercase
    MX: mixed case
    AN: all no case

    >>> get_label(u'Click')
    'IC'
    >>> get_label(u'F11')
    'AU'
    >>> get_label(u'OK')
    'AU'
    >>> get_label(u'/hone/Doc')
    'MX'
    >>> get_label(u'HealthCare')
    'MX'
    >>> get_label(u'ealthCare')
    'MX'
    >>> get_label(u'lower')
    'AL'
    >>> get_label(u'$123')
    'AN'
    >>> get_label(u'.')
    'AN'
    >>> get_label(u'Fb11')
    'IC'
    >>> get_label(u'11.5a')
    'AL'
    >>> get_label(u'11.5A')
    'AU'
    >>> get_label(u'11.5Aa')
    'MX'
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

def convert_to_trainable_format(raw_title, title_transform_func, doc = None):
    """
    Given some title(before capitalization), return the trainable(for CRF-suite) format
    
    >>> from util import make_capitalized_title
    >>> c = convert_to_trainable_format(u"CIS FMs hold summit in Belarus on Oct 10", make_capitalized_title)
    >>> c = convert_to_trainable_format(u"FTSE 100 watch: Footsie hits fresh lows on global growth concerns", make_capitalized_title)    
    >>> doc = open("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1", "r", "utf8").read()
    >>> c = convert_to_trainable_format(u"Why oil prices will be 'robust' long-term: Shell CEO", make_capitalized_title, doc)    
    
    Where    
    - the title word after being treated as title
    - At the title begining or not
    - the begining character is number or not
    - Lower case in dictionary or not
    - Upper case in dictionary or not
    - Capitalized in dictionary or not
    - Is all upper-case after removing the non-alphabetic symbols
    - Appear in document as capitalized or not(optional)
    - POS tags
    - the class label, "C" as "should be capitalized" and "L" should be "lowered"
    """
    words = nltk.word_tokenize(raw_title)    
    title_words = title_transform_func(title_words = words)
    
    feature_extractors = [get_alpha_label,
                          get_lower_in_dict_label,
                          get_upper_in_dict_label, 
                          get_cap_in_dict_label, 
                          get_allupper_label]
    
    pos_tags = [tag 
                for _, tag in nltk.pos_tag(words)] # pos tags

    if doc is not None:
        feature_extractors.append(appear_capitalized_indoc_label)
        
    head_title_word , head_word = title_words[0], words[0]

    features = [(head_title_word, "HEAD") + tuple([fe(head_word, doc = doc) for fe in feature_extractors]) + (pos_tags[0], get_label(head_word), )]
    features += [(title_word, "OTHER") + tuple([fe(word, doc = doc) for fe in feature_extractors]) + (pos_tags[i], get_label(word), )
                 for i, title_word, word in zip(xrange(1, len(title_words)), title_words[1:], words[1:])]

    return features

def print_trainable_data(path = "fnames_and_titles.txt", start = 50000, end = None,
                         content_extractor = get_document_content_paf,
                         title_transform_func = make_capitalized_title):
    i = 0
    with open(path, "r", "utf8") as f:
        for line in f:
            fname, title = json.loads(line)
            if i < start:
                i += 1
                continue
            
            if i % 1000 == 0:
                sys.stderr.write("Finished %d\n" %i)
            
            row = convert_to_trainable_format(title,
                                              title_transform_func,
                                              (content_extractor(fname) 
                                               if content_extractor and callable(content_extractor) 
                                               else None)
                                          )

            for stuff in row:
                print unicode(' '.join(stuff)).encode('utf8')
            print 
            
            i += 1

            if end is not None and i > end:
                sys.stderr.write("Reached %d.\nTerminate.\n" %(end))
                break

                
if __name__ == "__main__":
    import sys
    # import doctest
    # doctest.testmod()    
    # print_filenames_and_titles() 
    # print_trainable_data(start = 0, end = 30000)
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
    
    make_lowercase_title
    print_trainable_data(path = sys.argv[1],
                         start = start, end = end,
                         content_extractor = get_document_content,
                         title_transform_func = op_table[op])
    # path = "test-titles.txt",       
