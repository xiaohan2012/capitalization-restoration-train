from nltk.tag.hmm import HiddenMarkovModelTagger
from data import load_data

# load the train and test data
# (word1, tag1), (word2, tag2), ...
train_data = load_data(start = 0, end = 30000)
test_data = load_data(start = 30001, end = None)

print "Started HMM training & testing"

m = HiddenMarkovModelTagger.train(train_data, test_data)
