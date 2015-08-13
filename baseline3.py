"""
Baseline3:

- for each token in the title it finds all its mentions in the text
- if the token appears only in the title and never appears in the text  ==> it should be lower-cased, # why should it be lower-cased   ** UNREASONABLE **
- if the token appears in the text only at the beginning of the sentences ==> it stays as it is, i.e. capitalized   *NOT STRONG* 
- if the token at least once appeared in the text not at the beginning of the sentence and capitalized ==> it stays capitalized 
- if all mentions of the token in the text not at the beginning of the sentence are lower cased  ==> it should be lower-cased
- if the leading letter is non-alphabetical, return intact

Several questions:

- The first rule is unreasonable
- dictionary should be considered also(especially when the word doesn't appear in the document). 
  This means we need to select a good dictionary
- 

"""

import nltk


def appear_only_in_title(word, title, sents):
    """
    if the token appears only in the title and never appears in the text
p    
    word: the word
    title: the title words
    sents: list of list of str, the sent words
    
    >>> title = [u"Life", u"is", u"sometimes", u"miserable"]
    >>> doc = [[u"asdf", u"qwer", u"azasdf", u"Life", u"."]]
    >>> appear_only_in_title(u"Life", title, doc)
    False
    >>> appear_only_in_title(u"is", title, doc)
    True
    """
    assert (word in title), "The word should be a title word"
    
    for sent in sents:
        for w in sent:
            if w == word:
                return False
    return True


def appear_only_at_sentence_beginning(word, title, sents):
    """
    if the token appears in the text only at the beginning of the sentences

    >>> title = [u"Feng", u"Chao", u"Liang", u"Blah"]
    >>> doc = [[u"Feng", u"Chao", u"Liang", u"is", u"in", u"Wuhan", u"."], [u"Chao", u"Liang", u"is", u"not", u"."], [u"Liang", u"Chao", u"is", u"not", u"."]]
    >>> appear_only_at_sentence_beginning(u"Feng", title, doc)
    True
    >>> appear_only_at_sentence_beginning(u"Chao", title, doc)
    False
    >>> appear_only_at_sentence_beginning(u"Blah", title, doc)
    False
    """
    assert (word in title), "The word should be a title word"
    appear_at_sentence_beginning = False
    
    for sent in sents:
        sent_start = True
        for w in sent:
            if sent_start and w == word and word[0].isupper():
                appear_at_sentence_beginning = True
            elif w == word: # appeared cap in the middle of sentence
                return False
            sent_start = False
            
    if appear_at_sentence_beginning:
        return True
    else:
        return False


def appear_cap_in_sentence_middle(word, title, sents):
    """
    If the token at least once appeared in the text not at the beginning of the sentence and capitalized

    >>> title = [u"Feng", u"Chao", u"Liang", u"Blah", u"hehe"]
    >>> doc = [[u"Feng", u"Chao", u"Liang", u"is", u"in", u"Wuhan", u".", u"hehe"], [u"Chao", u"Liang", u"is", u"not", u"."], [u"Liang", u"Chao", u"is", u"not", u"."]]
    >>> appear_cap_in_sentence_middle(u"Feng", title, doc)
    False
    >>> appear_cap_in_sentence_middle(u"Chao", title, doc)
    True
    >>> appear_cap_in_sentence_middle(u"Blah", title, doc)
    False
    >>> appear_cap_in_sentence_middle(u"hehe", title, doc)
    False
    """
    assert (word in title), "The word should be a title word"
    
    for sent in sents:
        sent_start = True
        for w in sent:
            if not sent_start and w == word and w[0].isalpha() and w[0].isupper(): # appeared cap in the middle of sentence
                return True
            sent_start = False
            
    return False


def all_appear_lower_not_at_sentence_beginning(word, title, sents):
    """
    If all mentions of the token in the text not at the beginning of the sentence are lower cased

    >>> title = [u"Feng", u"Chao", u"Liang", u"Blah", u"hehe"]
    >>> doc = [[u"Feng", u"chao", u"Liang", u"is", u"in", u"Wuhan", u".", u"hehe"], [u"Chao", u"Liang", u"is", u"not", u"."], [u"Liang", u"Chao", u"is", u"not", u"."]]
    >>> all_appear_lower_not_at_sentence_beginning(u"hehe", title, doc)
    True
    >>> all_appear_lower_not_at_sentence_beginning(u"Chao", title, doc)
    False
    >>> all_appear_lower_not_at_sentence_beginning(u"Blah", title, doc)
    False
    >>> all_appear_lower_not_at_sentence_beginning(u"Feng", title, doc)
    False
    """
    assert (word in title), "The word should be a title word"

    appear_in_middle_lower = False
    for sent in sents:
        sent_start = True
        for w in sent:
            if not sent_start and w[0].isalpha() and w == word and w[0].isupper(): # appeared upper in the middle of sentence
                return False
            elif not sent_start and w[0].isalpha() and w == word and w[0].islower(): # appeared lower in the middle of sentence
                appear_in_middle_lower = True
            sent_start = False
    if appear_in_middle_lower:
        return True
    else:
        return False


def lower(word):
    return word[0].lower() + word[1:]


def cap(word):
    return word[0].upper() + word[1:]
    

def predict(title_words, doc_words):
    """
    Parameter:
    -----------
    title_words: list of string
    
    doc_words: list of list of string

    Return:
    ----------
    list of str: the labels
    """
    pass


def normalize_title(title = "", words = [], **kwargs):
    """
    >>> from util import make_capitalized_title
    >>> import nltk
    >>> from codecs import open
    
    >>> raw_words = nltk.word_tokenize(u"German equities end lively bourse session higher.")
    >>> cap_words = make_capitalized_title(title_words = raw_words)
    >>> doc_text = open("/cs/puls/tmp/Capitalization/reuters-text/42532newsML.txt", "r", "utf8").read()
    >>> normalize_title(words = cap_words, doc = doc_text)
    [u'German', u'equities', u'end', u'lively', u'bourse', u'session', u'higher', u'.']

    >>> raw_words = nltk.word_tokenize(u"FTSE 100 up, closes just below record as Dow slips.")
    >>> cap_words = make_capitalized_title(title_words = raw_words)
    >>> doc_text = open("/cs/puls/tmp/Capitalization/reuters-text/42558newsML.txt", "r", "utf8").read()
    >>> normalize_title(words = cap_words, doc = doc_text) # `Dow` is misclassified
    [u'FTSE', u'100', u'up', u',', u'closes', u'just', u'below', u'record', u'as', u'dow', u'slips', u'.']


    >>> raw_words = nltk.word_tokenize(u"Gold may see $400 before year-end - Merrill Lynch.")
    >>> cap_words = make_capitalized_title(title_words = raw_words)
    >>> doc_text = open("/cs/puls/tmp/Capitalization/reuters-text/42580newsML.txt", "r", "utf8").read()
    >>> normalize_title(words = cap_words, doc = doc_text) # 
    [u'Gold', u'may', u'see', u'$', u'400', u'before', u'year-end', u'-', u'Merrill', u'Lynch', u'.']

    """
    if title:
        words = nltk.word_tokenize(title)

    head = words[0][0].upper() + words[0][1:]
    tail = words[1:]

    doc = [[w for w in nltk.word_tokenize(sent)]
           for sent in nltk.sent_tokenize(kwargs["doc"])]

    normed_words = [head]

    for w in tail:
        if not w[0].isalpha(): # if no alpha, return intact
            normed_words.append(w)
        elif appear_only_in_title(w, words, doc) or all_appear_lower_not_at_sentence_beginning(w, words, doc):
            normed_words.append(lower(w))
        elif appear_only_at_sentence_beginning(w, words, doc):
            normed_words.append(w)
        elif appear_cap_in_sentence_middle(w, words, doc):
            normed_words.append(cap(w))
        else:
            raise ValueError("Unexpected case `%s` in `%r`" %(w, words))
    return normed_words



if __name__ == "__main__":
    import doctest
    doctest.testmod()
