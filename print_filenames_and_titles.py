import json
import nltk
from util import (get_file_names,
                  extract_title,
                  is_monocase,
                  normalize_title,
                  get_document_content_paf)

from guess_language import guessLanguage

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    """print title each per one line from the corpus"""
    
    year = 2014
    # months = ['01', '02', '03', '04', '05', '06', '07']  # 2015-08-05
    months = range(11, 13)
    # months = ['02'] # 2015-08-13
    # months = ['02', '03', '04', '05'], 2015-08-05
    # months = ['03']  # 2015-08-13
    
    days = xrange(1, 32)
    paths = ['/cs/puls/Corpus/Business/Puls/{}/{}/{:2d}/'.format(year, month, day)
             for month in months
             for day in days]

    collected = 0
    for i, fname in enumerate(get_file_names(paths)):
        if i % 100 == 0:
            logger.info("{} / {}".format(collected, i))

        try:
            title = extract_title(fname)
        except:
            logger.debug('Fail to find title')
            continue

        if not title:  # no title
            continue
            
        title = normalize_title(title)
        
        # is not monocase and is English
        if not is_monocase(nltk.word_tokenize(title)) and\
           guessLanguage(title) == "en":
            body = get_document_content_paf(fname)
            if len(body.strip()) > 0:  # non-empty
                collected += 1
                print json.dumps([fname, unicode(title).encode("utf8")])

if __name__ == "__main__":
    main()

