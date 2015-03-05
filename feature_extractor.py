import re, string
import enchant
import nltk
import string

class Feature(object):
    name = None
    
    @classmethod
    def get_value(cls, t, words, **kwargs):
        raise NotImplementedError

class WordFeature(Feature):
    """
    The word feature

    >>> WordFeature.get_value(0, ["company"])
    'company'
    """
    name = "word"

    @classmethod
    def get_value(cls, t, words, **kwargs):
        return words[t]


class POSFeature(Feature):
    """
    The word Part-of-speech tag

    >>> POSFeature.get_value(0, ["company"], pos = ["NN"])
    'NN'
    """
    name = "pos-tag"

    @classmethod
    def get_value(cls, t, words, **kwargs):
        if 'pos' in kwargs:
            return kwargs['pos'][t]
        else:
            raise KeyError("'pos' is not in arguments")

class IsLeadingWordFeature(Feature):
    """
    If the word is the first one of the sentence or not

    >>> IsLeadingWordFeature.get_value(1, ["company", "hehe"])
    False
    >>> IsLeadingWordFeature.get_value(0, ["123"])
    True
    """
    name = "is-leading-word"

    @classmethod
    def get_value(cls, t, words, **kwargs):
        return t == 0

class BeginsWithAlphaFeature(Feature):
    """
    If the word begins with alpha

    >>> BeginsWithAlphaFeature.get_value(0, ["company"])
    True
    >>> BeginsWithAlphaFeature.get_value(0, ["123"])
    False
    """
    name = "begins-with-alphabetic"

    @classmethod
    def get_value(cls, t, words, **kwargs):
        return words[t][0].isalpha()


d = enchant.Dict("en_US")

class LowercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary

    >>> LowercaseInDictionaryFeature.get_value(0, ["company"])
    True
    >>> LowercaseInDictionaryFeature.get_value(0, ["ibm"])
    False
    """

    name = "lower-in-dict"
    
    @classmethod
    def get_value(cls, t, words, **kwargs):
        return d.check(words[t].lower())

class UppercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary

    >>> UppercaseInDictionaryFeature.get_value(0, ["company"])
    True
    >>> UppercaseInDictionaryFeature.get_value(0, ["ibm"])
    True
    """

    name = "upper-in-dict"
    
    @classmethod
    def get_value(cls, t, words, **kwargs):
        return d.check(words[t].upper())

class OriginalInDictionaryFeature(Feature):
    """
    If the original word is in dictionary

    >>> OriginalInDictionaryFeature.get_value(0, ["Belarus"])
    True
    >>> OriginalInDictionaryFeature.get_value(0, ["belarus"])
    False
    """
    name = "orig-in-dict"
    
    @classmethod
    def get_value(cls, t, words, **kwargs):
        return d.check(words[t])

class ContainsPunctuationFeature(Feature):
    """
    If the word has punctuations

    >>> ContainsPunctuationFeature.get_value(0, ["A-B"])
    True
    >>> ContainsPunctuationFeature.get_value(0, ["AB"])
    False
    """
    name = "has-punct"
    
    punct = set(string.punctuation)
    @classmethod
    def get_value(cls, t, words, **kwargs):
        for l in words[t]:
            if l in cls.punct:
                return True
        return False

class CapitalizedInDictionaryFeature(Feature):
    """
    If the capitalized word is in dictionary

    >>> CapitalizedInDictionaryFeature.get_value(0, ["google"])
    True
    >>> CapitalizedInDictionaryFeature.get_value(0, ["ibm"])
    False
    """
    name = "cap-in-dict"
    
    @classmethod
    def get_value(cls, t, words, **kwargs):
        return d.check(words[t].capitalize())

class AllUppercaseFeature(Feature):
    """
    If the letters in word is all uppercased
    
    >>> AllUppercaseFeature.get_value(0, [u'U.S.'])
    True
    >>> AllUppercaseFeature.get_value(0, [u'Ad'])
    False
    >>> AllUppercaseFeature.get_value(0, [u'123..4'])
    False
    >>> AllUppercaseFeature.get_value(0, [u'HAO123'])
    True
    >>> AllUppercaseFeature.get_value(0, [u'FIIs'])    
    False
    """
    exclude = unicode(string.punctuation + ''.join([str(i) for i in xrange(10)]))
    table = {ord(c): None
             for c in exclude}
    name = "all-letter-uppercase"

    @classmethod
    def get_value(cls, t, words, **kwargs):
        word = words[t].translate(cls.table) # Remove punctuations + numbers
        if len(word) > 0:
            return (word.upper() == word)
        else:
            return False


DEFAULT_FEATURES = [
    WordFeature, IsLeadingWordFeature,
    LowercaseInDictionaryFeature,
    UppercaseInDictionaryFeature,
    CapitalizedInDictionaryFeature,
    OriginalInDictionaryFeature, 
    AllUppercaseFeature,
    BeginsWithAlphaFeature, 
    ContainsPunctuationFeature,
    POSFeature, 
]

# to solve the backward compatability issue
VALUE_LABEL_MAPPING = {
    IsLeadingWordFeature: {True: 'HEAD', False: 'OTHER'},
    LowercaseInDictionaryFeature: {True: 'LOWER_IN_DICT', False: 'OTHER'},
    CapitalizedInDictionaryFeature: {True: 'CAP_IN_DICT', False: 'OTHER'},
    UppercaseInDictionaryFeature: {True: 'UPPER_IN_DICT', False: 'OTHER'},
    OriginalInDictionaryFeature: {True: 'ORG_IN_DICT', False: 'OTHER'},
    BeginsWithAlphaFeature: {True: 'BEGINS_WITH_ALPHA', False: 'OTHER'},
    AllUppercaseFeature: {True: 'ALL_UPPER', False: 'OTHER'},
    ContainsPunctuationFeature: {True: 'HAS_PUNCT', False: 'OTHER'}
}

class FeatureExtractor(object):
    """
    Extract features for sentence

    >>> extractor = FeatureExtractor(transform_value = True)
    >>> info = extractor.extract([u"I", u"love", u"you"])
    >>> len(info[0]) == len(DEFAULT_FEATURES)
    True
    >>> info[0]["pos-tag"]
    'PRP'
    >>> info[0]["is-leading-word"]
    True
    >>> extractor.feature_names
    ['word', 'is-leading-word', 'lower-in-dict', 'upper-in-dict', 'cap-in-dict', 'orig-in-dict', 'all-letter-uppercase', 'begins-with-alphabetic', 'has-punct', 'pos-tag']
    """
    def __init__(self, features = DEFAULT_FEATURES, 
                 value_label_mapping = VALUE_LABEL_MAPPING, 
                 transform_value = False):
        self.features = features
        self.transform_value = transform_value

    def extract(self, sent):
        """Expect unicode strings"""
        if isinstance(sent, basestring): #if not tokenized
            sent = nltk.word_tokenize(sent)

        kwargs = {}
        if POSFeature in self.features:
            kwargs["pos"] = [tag for _, tag in nltk.pos_tag(sent)] # pos tags
                    
        words_with_features = []
        
        for i in xrange(len(sent)):
            word = {}
            for feature in self.features:
                word[feature.name] = feature.get_value(i, sent, **kwargs)                
            
            words_with_features.append(word)

        return words_with_features                                

    @property
    def feature_names(self):
        return [feature.name for feature in self.features]
