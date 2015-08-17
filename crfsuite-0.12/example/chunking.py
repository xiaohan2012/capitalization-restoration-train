#!/usr/bin/env python

"""
A feature extractor for chunking.
Copyright 2010,2011 Naoaki Okazaki.
"""
from capitalization_restoration.feature_templates import (lexical_features,
                                                          positional_features,
                                                          dict_features,
                                                          pos_features,
                                                          spelling_features,
                                                          document_features)
from capitalization_restoration.feature_extractor import DEFAULT_FEATURES


# Separator of field values.
separator = '\t'

id2feature = {
    1: lexical_features,
    2: positional_features,
    3: dict_features,
    4: pos_features,
    5: spelling_features,
    6: document_features
}

import crfutils

if __name__ == '__main__':
    import sys
    feature_ids = sys.argv[1]
    sys.stderr.write("Using feature groups: %r\n" % feature_ids)
    id2field = [feat.name
                for feat in DEFAULT_FEATURES]
    fields = [feat.name
              for feat in DEFAULT_FEATURES]
    fields.append('y')
    fields = " ".join(fields)
    
    templates = []

    for fid in feature_ids.split("+"):
        fid = int(fid.strip())
        templates += id2feature[fid]

    sys.stderr.write("Feature field names: %s\n" % fields)

    def feature_extractor(X):
        # Apply attribute templates to obtain features (in fact, attributes)
        crfutils.apply_templates(X, templates)
        if X:
            # Append BOS and EOS features manually
            X[0]['F'].append('__BOS__')     # BOS feature
            X[-1]['F'].append('__EOS__')    # EOS feature

    crfutils.main(feature_extractor, fields=fields, sep=separator)
