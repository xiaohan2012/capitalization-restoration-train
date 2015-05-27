import re
import string
import enchant
import nltk

from util import get_document_content_paf


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
        word = words[t].translate(cls.table)  # Remove punctuations + numbers
        if len(word) > 0:
            return (word.upper() == word)
        else:
            return False


class CapitalizedInDocumentFeature(Feature):
    """
    Whether the word appears capitalized in the document.

    One exception is the leading word of the sentence, which is capitalized by convention.

    In this case, we don't consider it as capitalized

    >>> from util import get_document_content_paf, get_document_content
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1")
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Shell"], doc=doc)
    True
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Van Beurden"], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Getty"], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u"'Getty"], doc=doc) #some trick
    False
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/12/www.sacbee.com.business.index/A33DCBDA991E786734BCA02B01B9DB04")
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Shinjiro'], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Valley'], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Robertson'], doc=doc)
    True
    """
    name = "indoccap"

    @classmethod
    def _get_label_for_word(cls, word, doc):
        if not word[0].isalpha():  # stuff like 'robust'
            return False

        word_capi = unicode(word[0].upper() + word[1:])
        regexp = re.compile(ur"[0-9a-zA-Z)] %s[ \t\n.,']" %
                            re.escape(word_capi), re.U)

        return True if regexp.search(doc) else False

    @classmethod
    def get_value(cls, t, words, **kwargs):
        doc = kwargs.get("doc")
        assert doc, "document string should be given"
        return cls._get_label_for_word(words[t], doc)

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
    CapitalizedInDocumentFeature
]


class FeatureExtractor(object):
    """
    Extract features for sentence

    >>> extractor = FeatureExtractor()
    >>> info = extractor.extract([u"I", u"love", u"you"], docpath="test_data/i-love-you")
    >>> len(info[0]) == len(DEFAULT_FEATURES)
    True
    >>> info[0]["pos-tag"]
    'PRP'
    >>> info[0]["is-leading-word"]
    True
    >>> info[1]["indoccap"]
    True
    >>> extractor.feature_names
    ['word', 'is-leading-word', 'lower-in-dict', 'upper-in-dict', 'cap-in-dict', 'orig-in-dict', 'all-letter-uppercase', 'begins-with-alphabetic', 'has-punct', 'pos-tag', 'indoccap']
    """
    def __init__(self, features=DEFAULT_FEATURES):
        self.features = features

    def extract(self, sent, *args, **kwargs):
        """Expect unicode strings"""
        assert isinstance(sent, list), "sent must be a list"

        feature_kwargs = {}

        if POSFeature in self.features:
            feature_kwargs["pos"] = [tag for _, tag in nltk.pos_tag(sent)]  # pos tags

        if CapitalizedInDocumentFeature in self.features:
            assert "docpath" in kwargs
            feature_kwargs["doc"] = get_document_content_paf(kwargs["docpath"])

        words_with_features = []

        for i in xrange(len(sent)):
            word = {}
            for feature in self.features:
                word[feature.name] = feature.get_value(i, sent,
                                                       **feature_kwargs)

            words_with_features.append(word)

        return words_with_features

    @property
    def feature_names(self):
        return [feature.name for feature in self.features]


class FeatureExtractorWithoutDocumentFeature(FeatureExtractor):
    def __init__(self):
        features = [WordFeature, IsLeadingWordFeature,
                    LowercaseInDictionaryFeature,
                    UppercaseInDictionaryFeature,
                    CapitalizedInDictionaryFeature,
                    OriginalInDictionaryFeature,
                    AllUppercaseFeature,
                    BeginsWithAlphaFeature,
                    ContainsPunctuationFeature,
                    POSFeature]
        super(FeatureExtractorWithoutDocumentFeature, self).__init__(features)
