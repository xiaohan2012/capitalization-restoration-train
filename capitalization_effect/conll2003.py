class CoNLLNERReader(object):
    u"""
    CoNLL2003 NER corpus reader
    
    >>> r = CoNLLNERReader("/cs/taatto/home/hxiao/capitalization-recovery/corpus/conll2003/eng.testa")
    >>> tagged_sents = r.read()
    >>> tagged_sents[0]
    [('CRICKET', 'O'), ('-', 'O'), ('LEICESTERSHIRE', 'I-ORG'), ('TAKE', 'O'), ('OVER', 'O'), ('AT', 'O'), ('TOP', 'O'), ('AFTER', 'O'), ('INNINGS', 'O'), ('VICTORY', 'O'), ('.', 'O')]
    >>> len(tagged_sents)
    3464
    """
    def __init__(self, path, field_keys = [0,3]):
        self.path = path
        self.field_keys = field_keys

    def read(self):
        started = False
        sents = []
        with open(self.path, "r") as f:
            for l in f:
                if l.startswith(u"-DOCSTART-"):
                    continue
                elif l.startswith("\n"): # newline
                    if not started:
                        started = True # enter here only once
                    else:
                        sents.append(sent)
                    sent = []
                else:
                    segs = l.strip().split()
                    sent.append(tuple(
                        [segs[key] for key in self.field_keys]
                    ))
            return sents
