import nltk
from feature_extractor import FeatureExtractor
from feature_templates import load_feature_templates
from cap_restore import MultiPurposeRestorer

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Restore the sentence capitalization relying on document content')
    parser.add_argument('-s', dest="sentence", type=str, required=True,
                        help='an integer for the accumulator')
    parser.add_argument('--docpath', type=str, required=True,
                        dest='docpath',
                        help='Path to the document associated with the sentence')

    args = parser.parse_args()

    kwargs={}
    kwargs['docpath'] = args.docpath

    r = MultiPurposeRestorer('models/cap_model.bin', 'models/lower_model.bin', 'models/upper_model.bin', FeatureExtractor(), load_feature_templates())
    print " ".join(r.restore(nltk.word_tokenize(unicode(args.sentence)), **kwargs))    
