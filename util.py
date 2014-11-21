"""
Util functions
"""
import os, re
from glob import glob
from codecs import open as decode_open

import nltk
import nltk.data

from ground_truth import (articles, prepositions, conjunctions)

def get_file_names(paths = ["/group/home/puls/Shared/capitalization-recovery/12"]):
    """
    Get all document file paths    
    """
    for path in paths:
        for doc_dir in glob(os.path.join(path, "*")):
            for file_path in glob(os.path.join(doc_dir, "*")):
                if (os.path.isfile(file_path) and "." not in os.path.basename(file_path)):
                    yield file_path

title_pos_regexp = re.compile(r"^(\d+) (\d+) Headline type main$")

def get_title_position(path):
    """
    >>> get_title_position("/group/home/puls/Shared/capitalization-recovery/30/online.wsj.com.xml.rss.3_7031/3918A8D35025B47AC6A62D293F5F506F.paf")
    (42, 77)
    """
    with decode_open(path, "r", "utf8") as paf:        
        for line in paf:
            match = title_pos_regexp.search(line)
            if match:
                # get title index
                start = int(match.group(1))
                end = int(match.group(2))
                return start, end

    raise Exception("Unable to find start and end position for %s" %path)
            

def get_document_content(path):
    """
    Exclude the title and get the actual content of the document

    >>> content = get_document_content("/group/home/puls/Shared/capitalization-recovery/12/www.ameinfo.com.rssfeeds.10660/DE01D30EA383DFD9FA1427CB9CC935F2")
    """
    _, end = get_title_position(path + ".paf")
    with decode_open(path, "r", "utf8", "ignore") as doc:
        doc.seek(end+1)
        return doc.read()

def extract_title(path):
    """
    Given document file path
    Extract the title 

    >>> extract_title("/group/home/puls/Shared/capitalization-recovery/12/www.ameinfo.com.rssfeeds.10660/DE01D30EA383DFD9FA1427CB9CC935F2")
    u'Polaroid launches new range of products at opening day of GITEX Technology Week 2014'
    >>> extract_title("/group/home/puls/Shared/capitalization-recovery/30/online.wsj.com.xml.rss.3_7031/3918A8D35025B47AC6A62D293F5F506F")
    u'Bad Bets Rock Fortress\u2019s Macro Fund'
    >>> extract_title("/group/home/puls/Shared/capitalization-recovery/30/feeds.foxbusiness.com.foxbusiness/E1D1899ED1CDEAB1574C1D279CBA2632")
    u'Is Gold\u2019s Knockout Punch Coming?'
    >>> extract_title("/group/home/puls/Shared/capitalization-recovery/30/www.streetinsider.com.freefeed.php/34D4137A7AEB5118C6E9EC451E66B529") 
    u'Solving IT Debuts on Staffing Industry Analysts\u2019 Top 100 Fastest-Growing U.S. Staffing and Talent Engagement Firms'
    """
    start, end = get_title_position(path + ".paf")
    with decode_open(path, "r", "utf8") as doc:
        #extract the content
        content = doc.read()
        return "".join(content[start: end])

def is_capitalized(title_words):
    """
    Determine if the title words are already capitalized

    >>> is_capitalized("Global Eagle Entertainment and SES Sign a Strategic Partnership to Deliver Global Ku-Band Satellite in-Flight Connectivity to Airlines".split())
    True
    >>> is_capitalized("Agenda Released for the 17th annual Summit on Superbugs & Superdrugs".split())
    False
    """
    for word in title_words[1:]:
        prefix = word.split("-")[0] #handle the in-Flight case
        should_be_lower = lambda w: w in articles or w in prepositions or w in conjunctions
        if should_be_lower(word) or should_be_lower(prefix):
            continue
        elif word[0].isalpha() and word[0].lower() == word[0]: # there is some lower cased words besides articles prepositions and conjunctions
            return False

    return True
    
def make_capitalized_title(title = None, title_words = None):
    """
    >>> make_capitalized_title(title = "This translation app helps professionals traveling in China and Japan")
    ['This', 'Translation', 'App', 'Helps', 'Professionals', 'Traveling', 'in', 'China', 'and', 'Japan']
    >>> make_capitalized_title(title = "Russia to see surge of investments if sanctions lifted: VTB Bank Head")
    ['Russia', 'to', 'See', 'Surge', 'of', 'Investments', 'if', 'Sanctions', 'Lifted', ':', 'VTB', 'Bank', 'Head']
    >>> make_capitalized_title(title = "CIS FMs hold summit in Belarus")
    ['CIS', 'FMs', 'Hold', 'Summit', 'in', 'Belarus']
    """
    
    trans_words = []
    if title_words:
        words = title_words
    elif title:
        words = nltk.word_tokenize(title)
    else:
        raise ValueError("Receive nothing..")

    for i, word in enumerate(words):
        if i == 0:
            trans_words.append(word if word[0] == word[0].upper() else word.capitalize())
        elif (word in articles or word in prepositions or word in conjunctions):
            trans_words.append(word)
        elif word[0] == word[0].upper(): #already capitalized
            trans_words.append(word)
        else:
            trans_words.append(word.capitalize())
    return trans_words

def transform_words(words, labels):
    """
    Transform words capitalization by labels

    >>> words = ['Google', '\\'s', 'Translation', 'App', 'Helps', 'Professionals', 'Traveling', 'in', 'China', 'and', 'Japan']
    >>> transform_words(words, ["C", "I", "L", "L", "L", "L", "L", "L", "C", "L", "C"])
    ['Google', "'s", 'translation', 'app', 'helps', 'professionals', 'traveling', 'in', 'China', 'and', 'Japan']
    """
    assert len(words) == len(labels)

    new_words = []
    for w, l in zip(words, labels):
        if l == "C":
            new_words.append(w[0].upper() + w[1:])
        elif l == "L":
            new_words.append(w[0].lower() + w[1:])
        elif l == "I":
            new_words.append(w)

    return new_words

if __name__ == "__main__":
    # path = get_file_names()[0]
    import doctest
    doctest.testmod()    
