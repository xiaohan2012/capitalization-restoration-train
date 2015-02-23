import re, string
import enchant
from util import get_document_content_paf

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
    """
    if not word[0].isalpha(): #stuff like 'robust'
        return "OTHER"
        
    word_upper = unicode(word[0].upper() + word[1:])
    regexp = re.compile(ur"[0-9a-zA-Z)] %s[ \t\n.,']" %re.escape(word_upper), re.U)
    return "IN_DOC_CAP" if regexp.search(doc) else "OTHER"

def appear_lower_indoc_label(word, doc):
    pass


def appear_upper_indoc_label(word, doc):
    pass

def get_alpha_label(word, **kwargs):
    return "BEGINS_WITH_ALPHA" if word[0].isalpha() else "OTHER"    


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
