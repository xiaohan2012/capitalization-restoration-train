# -*- coding: utf-8 -*-

import sys, re, json

import enchant
import nltk
from codecs import open

from util import (get_file_names, 
                  extract_title, 
                  make_capitalized_title, 
                  get_document_content, 
                  is_capitalized)

from ground_truth import (articles, prepositions, conjunctions)

def is_capitalized(s):
    for w in s.split():
        if w not in articles and w not in prepositions and w not in conjunctions:
            if w[0] != w[0].upper():
                return False
    return True

def print_filenames_and_titles():
    """print title each per one line from the corpus"""
    paths = ['/group/home/puls/Shared/capitalization-recovery/%2d' %i 
             for i in xrange(9, 32)]    
    titles = []
    for fname in get_file_names(paths):
        title = extract_title(fname)
        if not is_capitalized(title):
            print json.dumps([fname, unicode(title).encode("utf8")])
    

def get_alpha_label(word, **kwargs):
    return "BEGINS_WITH_ALPHA" if word[0].isalpha() else "OTHER"    

def appear_capitalized_indoc_label(word, doc):
    """
    >>> doc = get_document_content("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1")
    >>> appear_capitalized_indoc_label(u"Shell", doc)
    'IN_DOC_CAP'
    >>> appear_capitalized_indoc_label(u"Van Beurden", doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u"Getty", doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u"'Getty", doc) #some trick
    'OTHER'
    >>> doc = get_document_content("/group/home/puls/Shared/capitalization-recovery/12/www.sacbee.com.business.index/A33DCBDA991E786734BCA02B01B9DB04")
    >>> appear_capitalized_indoc_label(u'Shinjiro', doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u'Valley', doc)
    'OTHER'
    >>> appear_capitalized_indoc_label(u'Robertson', doc)
    'IN_DOC_CAP'
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
    
def get_label(word, **kwargs):
    if word[0].isalpha() and word[0] == word[0].upper():
        return "C" 
    elif word[0].isalpha():
        return "L"
    else:
        return "I"

def convert_to_trainable_format(raw_title, doc = None):
    """
    Given some title(before capitalization), return the trainable format
    
    >>> convert_to_trainable_format("CIS FMs hold summit in Belarus on Oct 10")
    [('CIS', 'HEAD', 'BEGINS_WITH_ALPHA', 'OTHER', 'OTHER', 'OTHER', 'C'), ('FMs', 'OTHER', 'BEGINS_WITH_ALPHA', 'OTHER', 'OTHER', 'OTHER', 'C'), ('Hold', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Summit', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('in', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Belarus', 'OTHER', 'BEGINS_WITH_ALPHA', 'OTHER', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'C'), ('on', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Oct', 'OTHER', 'BEGINS_WITH_ALPHA', 'OTHER', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'C'), ('10', 'OTHER', 'OTHER', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'I')]
    >>> convert_to_trainable_format("FTSE 100 watch: Footsie hits fresh lows on global growth concerns")
    [('FTSE', 'HEAD', 'BEGINS_WITH_ALPHA', 'OTHER', 'OTHER', 'OTHER', 'C'), ('100', 'OTHER', 'OTHER', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'I'), ('Watch', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), (':', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'I'), ('Footsie', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'C'), ('Hits', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Fresh', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Lows', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('on', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Global', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Growth', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L'), ('Concerns', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'L')]
    >>> doc = open("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1", "r", "utf8").read()
    >>> convert_to_trainable_format("Why oil prices will be 'robust' long-term: Shell CEO", doc)
    [('Why', 'HEAD', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'C'), ('Oil', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'L'), ('Prices', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'L'), ('Will', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'L'), ('Be', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'L'), ("'robust", 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'I'), ("'", 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'I'), ('Long-term', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'OTHER', 'L'), (':', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'OTHER', 'I'), ('Shell', 'OTHER', 'BEGINS_WITH_ALPHA', 'LOWER_IN_DICT', 'UPPER_IN_DICT', 'CAP_IN_DICT', 'IN_DOC_CAP', 'C'), ('CEO', 'OTHER', 'BEGINS_WITH_ALPHA', 'OTHER', 'UPPER_IN_DICT', 'OTHER', 'IN_DOC_CAP', 'C')]
    
    Where    
    - the title word after being treated as title
    - At the title begining or not
    - the begining character is number or not
    - Lower case in dictionary or not
    - Upper case in dictionary or not
    - Capitalized in dictionary or not
    - Appear in document as capitalized or not(optional)
    
    - the class label, "C" as "should be capitalized" and "L" should be "lowered"
    """
    words = nltk.word_tokenize(raw_title)    
    title_words = make_capitalized_title(title_words = words)
    
    feature_extractors = [get_alpha_label,
                          get_lower_in_dict_label,
                          get_upper_in_dict_label, 
                          get_cap_in_dict_label]
    
    if doc:
        feature_extractors.append(appear_capitalized_indoc_label)
        
    head_title_word , head_word = title_words[0], words[0]
    
    return [(head_title_word, "HEAD") + tuple([fe(head_word, doc = doc) for fe in feature_extractors]) + (get_label(head_word), )] + \
        [(title_word, "OTHER") + tuple([fe(word, doc = doc) for fe in feature_extractors]) + (get_label(word), )
         for title_word, word in zip(title_words[1:], words[1:])]

def load_data(start, end, path = "fnames_and_titles.txt"):
    """
    Return data in format like:
    [
    [(word1, tag1), (word2, tag2), ...], #sentence 1
    [(word1, tag1), (word2, tag2), ...], #sentence 2
    ]
    """
    print "loading data indexed from %d to %r" %(start, end)
    i = 0
    data = []
    with open(path, "r", "utf8") as f:
        for line in f:
            if i < start:
                i += 1
                continue

            _, title = json.loads(line)

            if i % 1000 == 0:
                print "Finished %d" %(i)
            
            words = nltk.word_tokenize(title)

            if is_capitalized(words): # Ignore those that are capitalized
                continue
                
            title_words = make_capitalized_title(title_words = words)
            labels = [get_label(word) for word in words]
            data.append(zip(title_words, labels))

            i += 1
            if end is not None and i > end:
                sys.stderr.write("Reached %d.\nTerminate.\n" %(end))
                break
                
    return data

def print_trainable_data(path = "fnames_and_titles.txt", start = 50000, end = None):
    i = 0
    with open(path, "r", "utf8") as f:
        for line in f:
            fname, title = json.loads(line)
            if i < start:
                i += 1
                continue
            
            if i % 1000 == 0:
                sys.stderr.write("Finished %d\n" %i)

            row = convert_to_trainable_format(title, get_document_content(fname))
            
            for stuff in row:
                print unicode(' '.join(stuff)).encode('utf8')
            print 
            
            i += 1

            if end is not None and i > end:
                sys.stderr.write("Reached %d.\nTerminate.\n" %(end))
                break

                
if __name__ == "__main__":
    import doctest
    doctest.testmod()    
    # print_filenames_and_titles() 
    # print_trainable_data(start = 0, end = 50000)
    # print_trainable_data(start = 50001, end = None)
    # path = "test-titles.txt", 

        
