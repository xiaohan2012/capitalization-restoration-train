import nltk
import pycrfsuite
from feature_extractor import FeatureExtractor
from feature_templates import (load_feature_templates, apply_templates)

tagger = pycrfsuite.Tagger()
tagger.open("/cs/taatto/home/hxiao/capitalization-recovery/result/training_size/cap/30000/model")


extractor = FeatureExtractor(transform_value = True)
templates = load_feature_templates()

def restore(sent):
    """
    >>> restore(u"Hedge Funds Muscle into Reinsurance, Attracting Doubters")
    
    """
    words_with_features = extractor.extract(sent)

    for word in words_with_features: # accord to crfsuite 
        word["F"] = []
            
    return tagger.tag(apply_templates(words_with_features, templates))
    
