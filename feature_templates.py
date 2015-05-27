import sys
# Attribute templates.

lexical_features = [ 
    (('word',  1), ),
    (('word',  -1), ),
    (('word',  0), ),
    (('word', -1), ('word',  0)),
    (('word',  0), ('word',  1)),
]

positional_features = [
    (('is-leading-word', 0), ),
]

dict_features = [
    (('lower-in-dict', 0), ),
    (('upper-in-dict', 0), ),
    (('cap-in-dict', 0), ),
    (('orig-in-dict', 0), ),
]

pos_features = [
    (('pos-tag',  1), ),
    (('pos-tag',  -1), ),
    (('pos-tag',  0), ),
    (('pos-tag', -1), ('pos-tag',  0)),
    (('pos-tag',  0), ('pos-tag',  1)),
]

spelling_features = [
    (('all-letter-uppercase', 0), ),
    (('begins-with-alphabetic', 0), ),
    (('has-punct', 0), )
]

document_features = [(('indoccap', 0), )]

id2featue = {
    1: lexical_features,
    2: positional_features,
    3: dict_features,
    4: pos_features,
    5: spelling_features,
    6: document_features
}

def load_feature_templates(feature_ids = [1,2,3,4,5,6]):
    templates = []

    for fid in feature_ids:
        templates += id2featue[fid]

    return templates

def apply_templates(X, templates):
    """
    Generate features for an item sequence by applying feature templates.
    A feature template consists of a tuple of (name, offset) pairs,
    where name and offset specify a field name and offset from which
    the template extracts a feature value. Generated features are stored
    in the 'F' field of each item in the sequence.

    @type   X:      list of mapping objects
    @param  X:      The item sequence.
    @type   template:   tuple of (str, int)
    @param  template:   The feature template.
    """
    for template in templates:
        name = '|'.join(['%s[%d]' % (f, o) for f, o in template])
        for t in range(len(X)):
            values = []
            for field, offset in template:
                p = t + offset
                if p not in range(len(X)):
                    values = []
                    break
                values.append(str(X[p][field]))
            if values:
                X[t]['F'].append('%s=%s' % (name, '|'.join(values)))

    if X:
        # Append BOS and EOS features manually
        X[0]['F'].append('__BOS__')     # BOS feature
        X[-1]['F'].append('__EOS__')    # EOS feature

    return [x["F"] for x in X] #get the F out
