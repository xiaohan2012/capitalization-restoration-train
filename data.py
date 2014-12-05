# -*- coding: utf-8 -*-

import sys, re, json, string

import enchant
import nltk
from codecs import open
from guess_language import guessLanguage

from util import (get_file_names, 
                  extract_title, 
                  make_capitalized_title,
                  make_uppercase_title, 
                  get_document_content_paf,
                  get_document_content, 
                  is_monocase, 
                  normalize_title)

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
    

def get_alpha_label(word, **kwargs):
    return "BEGINS_WITH_ALPHA" if word[0].isalpha() else "OTHER"    

def appear_capitalized_indoc_label(word, doc):
    """
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1")
    >>> appear_capitalized_indoc_label(u"Shell", doc)
    'IN_DOC_CAP'
    >>> appear_capitalized_indoc_label(u"Van Beurden", doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u"Getty", doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u"'Getty", doc) #some trick
    'OTHER'
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/12/www.sacbee.com.business.index/A33DCBDA991E786734BCA02B01B9DB04")
    >>> appear_capitalized_indoc_label(u'Shinjiro', doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u'Valley', doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u'Robertson', doc)
    'IN_DOC_CAP'
    >>> doc = get_document_content("data/empty.txt")
    >>> appear_capitalized_indoc_label(u'stuff', doc)
    'OTHER'
    """
    if not word[0].isalpha(): #stuff like 'robust'
        return "OTHER"
        
    word_upper = unicode(word[0].upper() + word[1:])
    regexp = re.compile(ur"[0-9a-zA-Z)] %s[ \t\n.,']" %re.escape(word_upper), re.U)
    
    return "IN_DOC_CAP" if regexp.search(doc) else "OTHER"

d = enchant.Dict("en_US")
def get_lower_in_dict_label(word, **kwargs):
    if d.check(word.lower()):
        return "LOWER_IN_DICT"
    else:
        return "OTHER"

def get_upper_in_dict_label(word, **kwargs):
    if d.check(word.upper()):
        return "UPPER_IN_DICT"
    else:
        return "OTHER"

def get_cap_in_dict_label(word, **kwargs):
    if d.check(word.capitalize()):
        return "CAP_IN_DICT"
    else:
        return "OTHER"


exclude = unicode(string.punctuation + ''.join([str(i) for i in xrange(10)]))
table = {ord(c): None
         for c in exclude}

def get_allupper_label(word, **kwargs):
    """
    If the letters in word is all uppercased
    
    >>> get_allupper_label(u'U.S.')
    'ALL_UPPER'
    >>> get_allupper_label(u'Ad')
    'OTHER'
    >>> get_allupper_label(u'123..4')
    'OTHER'
    >>> get_allupper_label(u'HAO123')
    'ALL_UPPER'
    >>> # get_allupper_label(u'FIIs')    
    """
    word = word.translate(table) # Remove punctuations + numbers
    if word and word.upper() == word:
        return "ALL_UPPER"
    else:
        return "OTHER"
    
def get_label(word, **kwargs):
    """
    >>> get_label(u'GCC')
    'I'
    >>> get_label(u'Kinder')
    'C'
    >>> get_label(u'213')
    'I'
    >>> get_label(u'lower')
    'L'
    >>> get_label(u'U.S.')
    'I'
    >>> get_label(u'\\'s')
    'I'
    >>> # get_label(u'in-Flight')
    """
    if word.upper() == word:
        return "I"
    elif word[0].isalpha() and word[0] == word[0].upper():
        return "C" 
    elif word[0].isalpha():
        return "L"
    else:
        return "I"
        # raise ValueError("Invalid value `%s`" %(word))

def convert_to_trainable_format(raw_title, title_transform_func, doc = None):
    """
    Given some title(before capitalization), return the trainable format
    
    >>> c = convert_to_trainable_format(u"CIS FMs hold summit in Belarus on Oct 10")
    >>> c = convert_to_trainable_format(u"FTSE 100 watch: Footsie hits fresh lows on global growth concerns")    
    >>> doc = open("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1", "r", "utf8").read()
    >>> c = convert_to_trainable_format(u"Why oil prices will be 'robust' long-term: Shell CEO", doc)    
    
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
    
    return [(head_title_word, "HEAD") + tuple([fe(head_word, doc = doc) for fe in feature_extractors]) + (pos_tags[0], get_label(head_word), )] + \
        [(title_word, "OTHER") + tuple([fe(word, doc = doc) for fe in feature_extractors]) + (pos_tags[i], get_label(word), )
         for i, title_word, word in zip(xrange(1, len(title_words)), title_words[1:], words[1:])]

def print_trainable_data(path = "fnames_and_titles.txt", start = 50000, end = None,
                         content_extractor = get_document_content_paf,
                         title_transform_func = make_capitalized_title):
    i = 0
    with open(path, "r", "utf8") as f:
        for line in f:
            fname, title = json.loads(line)
            fname = "/cs/puls/tmp/Capitalization/reuters-text/" + fname
            if i < start:
                i += 1
                continue
            
            if i % 1000 == 0:
                sys.stderr.write("Finished %d\n" %i)

            row = convert_to_trainable_format(title,
                                              title_transform_func,
                                              content_extractor(fname))
            
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
    print_trainable_data(path = sys.argv[1],
                         start = 0, end = None,
                         content_extractor = get_document_content,
                         title_transform_func = make_uppercase_title)
    # path = "test-titles.txt",       
