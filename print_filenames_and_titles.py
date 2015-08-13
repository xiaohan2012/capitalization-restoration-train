import sys
import json
import nltk
from util import (get_file_names,
                  extract_title,
                  is_monocase,
                  normalize_title)

from guess_language import guessLanguage


def main():
    """print title each per one line from the corpus"""
    
    # months = ['04', '05'], 2015-08-05
    # months = ['02'] # 2015-08-13
    months = ['03']  # 2015-08-13
    
    days = xrange(1, 32)
    paths = ['/cs/puls/Corpus/Business/Puls/2015/{}/{:2d}/'.format(month, day)
             for month in months
             for day in days]

    for fname in get_file_names(paths):
        try:
            title = extract_title(fname)
        except:
            sys.stderr.write('Fail to find title')
            continue

        if not title:  # no title
            continue
            
        title = normalize_title(title)
        
        # is not monocase and is English
        if not is_monocase(nltk.word_tokenize(title)) and\
           guessLanguage(title) == "en":
            print json.dumps([fname, unicode(title).encode("utf8")])

if __name__ == "__main__":
    main()
