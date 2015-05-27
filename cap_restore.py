import sys
import nltk
import pycrfsuite
from feature_extractor import FeatureExtractor
from feature_templates import (load_feature_templates, apply_templates)

from cap_detect import (capitalized, all_lowercase, all_uppercase)

_CAPRESTORER = None
_LOWERRESTORER = None
_UPPERRESTORER = None

def restore(words, *args, **kwargs):
    """
    Restore the capitalization of given words
    
    >>> restore(nltk.word_tokenize(u"Hedge Funds Muscle into Reinsurance, Attracting Doubters"))
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> restore(nltk.word_tokenize(u"HEDGE FUNDS MUSCLE INTO REINSURANCE, ATTRACTING DOUBTERS")) # doctest: +SKIP
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> restore(nltk.word_tokenize(u"hedge funds muscle into reinsurance, attracting doubters"))
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    >>> restore(nltk.word_tokenize(u"Hedge funds muscle into reinsurance, attracting doubters")) # properly capitalized
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    """
    global _CAPRESTORER
    global _LOWERRESTORER
    global _UPPERRESTORER
    
    if capitalized(words):
        if not _CAPRESTORER:
            _CAPRESTORER = CapRestorer()
        return _CAPRESTORER.restore(words, *args, **kwargs)
    elif all_lowercase(words):
        if not _LOWERRESTORER:
            _LOWERRESTORER = LowerRestorer()
        return _LOWERRESTORER.restore(words, *args, **kwargs)
    elif all_uppercase(words):
        if not _UPPERRESTORER:
            _UPPERRESTORER = UpperRestorer()
        return _UPPERRESTORER.restore(words, *args, **kwargs)
    else:
        sys.stderr.write("Seems to be in proper capitalization\n")
        return words

class Restorer(object):
    def __init__(self, model_path):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model_path)
        self.extractor = FeatureExtractor()
        self.templates = load_feature_templates()

    def get_labels(self, sent, *args, **kwargs):
        assert isinstance(sent, list)
        
        words_with_features = self.extractor.extract(sent, *args, **kwargs)

        for word in words_with_features: # accord to crfsuite 
            word["F"] = []
               
        return self.tagger.tag(apply_templates(words_with_features, self.templates))

    def restore(self, sent, *args, **kwargs):
        labels = self.get_labels(sent, *args, **kwargs)
        return transform_words_by_labels(sent, labels)

class CapRestorer(Restorer):
    """
    >>> words = nltk.word_tokenize(u"Hedge Funds Muscle into Reinsurance, Attracting Doubters")
    >>> r = CapRestorer()
    >>> r.restore(words) 
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    """
    def __init__(self):
        super(CapRestorer, self).__init__("models/cap_model.bin")

class LowerRestorer(Restorer):
    """
    >>> words = nltk.word_tokenize(u"hedge funds muscle into reinsurance, attracting doubters")
    >>> r = LowerRestorer()
    >>> r.restore(words) 
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    """
    def __init__(self):
        super(LowerRestorer, self).__init__("models/lower_model.bin")

class UpperRestorer(Restorer):
    """
    >>> words = nltk.word_tokenize(u"HEDGE FUNDS MUSCLE INTO REINSURANCE, ATTRACTING DOUBTERS")
    >>> r = UpperRestorer()
    >>> r.restore(words) # doctest: +SKIP
    [u'Hedge', u'funds', u'muscle', u'into', u'reinsurance', u',', u'attracting', u'doubters']
    """
    def __init__(self):
        super(UpperRestorer, self).__init__("models/upper_model.bin")


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Restore the sentence capitalization')
    parser.add_argument('-s', dest="sentence", type=str, required=True,
                        help='an integer for the accumulator')
    parser.add_argument('--docpath', type=str, required=False,
                        help='Path to the document associated with the sentence')

    args = parser.parse_args()

    kwargs={}
    if parser.docpath:
        kwargs['docpath'] = parser.docpath

    restore(parser.sentence, **kwargs)

        
