import sys
import nltk
import pycrfsuite
from feature_extractor import (FeatureExtractor,
                               WordFeature,
                               IsLeadingWordFeature,
                               LowercaseInDictionaryFeature,
                               UppercaseInDictionaryFeature,
                               CapitalizedInDictionaryFeature,
                               OriginalInDictionaryFeature,
                               AllUppercaseFeature,
                               BeginsWithAlphaFeature,
                               ContainsPunctuationFeature,
                               POSFeature)
from feature_templates import (load_feature_templates, apply_templates)

from cap_detect import (capitalized, all_lowercase, all_uppercase)


class MultiPurposeRestorer(object):
    """
    Capitalization restorer that captures capitalized, lowercase and uppercase sentences

    >>> feature_extractor = FeatureExtractor([WordFeature, IsLeadingWordFeature, LowercaseInDictionaryFeature, UppercaseInDictionaryFeature, CapitalizedInDictionaryFeature, OriginalInDictionaryFeature, AllUppercaseFeature, BeginsWithAlphaFeature, ContainsPunctuationFeature, POSFeature])
    >>> feature_templates = load_feature_templates([1,2,3,4,5])
    >>> r = MultiPurposeRestorer('models/cap_model_no_capindoc.bin', 'models/lower_model_no_capindoc.bin', 'models/upper_model_no_capindoc.bin', feature_extractor, feature_templates)
    >>> r.restore(nltk.word_tokenize(u"Hedge Funds Muscle into Reinsurance, Attracting Doubters"))
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> r.restore(nltk.word_tokenize(u"HEDGE FUNDS MUSCLE INTO REINSURANCE, ATTRACTING DOUBTERS")) # doctest: +SKIP
    [u'HEDGE', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> r.restore(nltk.word_tokenize(u"hedge funds muscle into reinsurance, attracting doubters"))
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> r.restore(nltk.word_tokenize(u"Hedge funds muscle into reinsurance, attracting doubters")) # properly capitalized
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']


    >>> r = MultiPurposeRestorer('models/cap_model.bin', 'models/lower_model.bin', 'models/upper_model.bin', FeatureExtractor(), load_feature_templates())
    >>> r.restore(nltk.word_tokenize(u"Cyan Holdings Represented at Heavyweight Round-table Event in India"), docpath="/group/home/puls/Shared/capitalization-recovery/10/www.proactiveinvestors.co.uk.sectors.41.rss/D8B4C87CDC7862F53E6285DDC892C7C0")
    [u'Cyan', u'Holdings', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'India']
    >>> r.restore(nltk.word_tokenize(u"cyan holdings represented at heavyweight round-table event in india"), docpath="/group/home/puls/Shared/capitalization-recovery/10/www.proactiveinvestors.co.uk.sectors.41.rss/D8B4C87CDC7862F53E6285DDC892C7C0")
    [u'Cyan', u'Holdings', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'India']
    >>> r.restore(nltk.word_tokenize(u"CYAN HOLDINGS REPRESENTED AT HEAVYWEIGHT ROUND-TABLE EVENT IN INDIA"), docpath="/group/home/puls/Shared/capitalization-recovery/10/www.proactiveinvestors.co.uk.sectors.41.rss/D8B4C87CDC7862F53E6285DDC892C7C0") # doctest: +SKIP
    [u'CYAN', u'HOLDINGS', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'INDIA']
    """
    def __init__(self, cap_model_path, lower_model_path, upper_model_path,
                 feature_extractor, feature_templates):
        self.cap_restorer = Restorer(cap_model_path, feature_extractor,
                                     feature_templates)
        self.lower_restorer = Restorer(lower_model_path, feature_extractor,
                                       feature_templates)
        self.upper_restorer = Restorer(upper_model_path, feature_extractor,
                                       feature_templates)

    def _get_restorer(self, words):
        if all_lowercase(words):
            return self.lower_restorer
        elif all_uppercase(words):
            return self.upper_restorer
        elif capitalized(words):
            return self.cap_restorer
        else:
            return None

    def restore(self, words, *args, **kwargs):
        restorer = self._get_restorer(words)
        if restorer:
            return restorer.restore(words, *args, **kwargs)
        else:
            sys.stderr.write("Seems to be in proper capitalization\n")
            return words

class Restorer(object):
    def __init__(self, model_path,
                 feature_extractor=FeatureExtractor(),
                 feature_templates=load_feature_templates()):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model_path)
        self.extractor = feature_extractor
        self.templates = feature_templates

    def get_labels(self, sent, *args, **kwargs):
        assert isinstance(sent, list)

        words_with_features = self.extractor.extract(sent, *args, **kwargs)

        for word in words_with_features: # accord to crfsuite 
            word["F"] = []

        return self.tagger.tag(apply_templates(words_with_features, self.templates))

    def restore(self, sent, *args, **kwargs):
        labels = self.get_labels(sent, *args, **kwargs)
        return transform_words_by_labels(sent, labels)


def transform_words_by_labels(words, labels):
    """
    Transform words capitalization by labels

    >>> words = [u'I', u'Compared', u'PaaS', u'Providers', u':', u'Heroku', u'and', u"IBM", u"'s", u'Bluemix', u'.']
    >>> transform_words_by_labels(words, [u'AU', u'AL', u'MX', u'AL', u'AN', u'IC', u'AL', u'AU', u'AL', u'IC', u'AN'])
    [u'I', u'compared', u'PaaS', u'providers', u':', u'Heroku', u'and', u'IBM', u"'s", u'Bluemix', u'.']
    """
    assert len(words) == len(labels)

    new_words = []
    for w, l in zip(words, labels):
        if l == "IC":
            new_words.append(w[0].upper() + w[1:])
        elif l == "AL":
            new_words.append(w.lower())
        elif l == "AU":
            new_words.append(w.upper())
        elif l == "MX" or l == "AN": # TODO: handle more complex cases for all uppercase or all lowercase input
            new_words.append(w)
        else:
            raise ValueError("Unknown label %s" %(l))

    return new_words
