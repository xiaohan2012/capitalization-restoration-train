# -*- coding: utf-8 -*-

"""
Util functions
"""
import os, re, sys, traceback
import logging
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt = "%H:%M:%S")

from glob import glob
from codecs import open as decode_open

import nltk
import nltk.data

import lxml
from pyquery import PyQuery as pq

from zipfile import ZipFile
import json

from ground_truth import (ARTICLES, PREPOSITIONS, CONJUNCTIONS)

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
            
def get_document_content_paf(path):
    """
    Content extractor for PAF file
    Exclude the title and get the actual content of the document

    >>> c = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/30/online.wsj.com.xml.rss.3_7031/3918A8D35025B47AC6A62D293F5F506F")
    """
    _, end = get_title_position(path + ".paf")
    with decode_open(path, "r", "utf8", "ignore") as doc:
        content = doc.read()
        return "".join(content[end:])

def get_document_content(path):
    """
    Get the actual content of the document

    >>> get_document_content("/home/group/puls/Shared/capitalization-recovery/reuters-text/sth.txt")
    u'something'
    """
    with decode_open(path, "r", "utf8", "ignore") as doc:
        return doc.read()

def is_monocase(title_words):
    """
    Determine if the title words are already capitalized

    >>> is_monocase("Global Eagle Entertainment and SES Sign a Strategic Partnership to Deliver Global Ku-Band Satellite in-Flight Connectivity to Airlines".split())
    True
    >>> is_monocase("Agenda Released for the 17th annual Summit on Superbugs & Superdrugs".split())
    False
    >>> is_monocase("How Find Your Inner Martin Scorsese to Build Brand & Rule the World".split())
    True
    >>> is_monocase("Half of YouTube's Traffic is Now Coming From Mobile: CEO".split()) # `is`
    True
    >>> is_monocase("Crystal Bridges Announces 2015 Exhibits, Including Warhol, van Gogh, Pollock".split()) # `van`
    True
    """
    for word in title_words[1:]:
        prefix = word.split("-")[0] #handle the in-Flight case
        should_be_lower = lambda w: (w in ARTICLES or
                                     w in PREPOSITIONS or
                                     w in CONJUNCTIONS)

        if should_be_lower(word) or should_be_lower(prefix):
            continue
        elif word[0].isalpha() and word[0].lower() == word[0]: # there is some lower cased words besides articles prepositions and conjunctions
            return False

    return True

# Mapping for non-standard punctuations to standard ones

trans_mapping = {u'‘': u'\'',# (8216 ‘ #\LEFT_SINGLE_QUOTATION_MARK)
             u'’': u'\'',# (8217 ’ #\RIGHT_SINGLE_QUOTATION_MARK)
             u'❛': u'\'',# (10075 #\HEAVY_SINGLE_TURNED_COMMA_QUOTATION_MARK_ORNAMENT)
             u'❜': u'\'',# (10076 #\HEAVY_SINGLE_COMMA_QUOTATION_MARK_ORNAMENT)
             u'\u0092': u'\'', # (146 #\Private-Use-Two)
             u'‛': u'\'',    # (8219 ‛ #\SINGLE_HIGH-REVERSED-9_QUOTATION_MARK)
             u'“': u'"',  # (8220 “ #\LEFT_DOUBLE_QUOTATION_MARK)
             u'”': u'"',  # (8221 ” #\RIGHT_DOUBLE_QUOTATION_MARK)
             u'‟': u'"',  # (8223 ‟ #\DOUBLE_HIGH-REVERSED-9_QUOTATION_MARK)
             u'❝': u'"',  # (10077 ❝ #\HEAVY_DOUBLE_TURNED_COMMA_QUOTATION_MARK_ORNAMENT)
             u'❞': u'"', # (10078 ❞ #\HEAVY_DOUBLE_COMMA_QUOTATION_MARK_ORNAMENT)
             u'＂': u'"', # (65282 ＂ #\FULLWIDTH_QUOTATION_MARK)
             u'＇': u'\'', # (65287 ＇ #\FULLWIDTH_APOSTROPHE)
             u'，': u',', # (65292 #\FULLWIDTH_COMMA)
             u'_': u' ', # (95 UNDERSCORE)
             u'–': u'-', # (8211 #\EN_DASH)
             u'—': u'-', # (8212 #\EM_DASH)
         }
trans_table = {ord(f): t
               for f,t in trans_mapping.items()}
    
def normalize_title(s):
    """
    >>> normalize_title(u'Bad Bets Rock Fortress\u2019s Macro Fund')
    u"Bad Bets Rock Fortress's Macro Fund"
    >>> normalize_title(u'Is Gold\u2019s Knockout Punch Coming?')
    u"Is Gold's Knockout Punch Coming?"
    >>> normalize_title(u'Judge finds flaw in Sacramento\u0092s arena review, but construction will continue')
    u"Judge finds flaw in Sacramento's arena review, but construction will continue"
    """    
    try:
        return s.translate(trans_table)
    except:
        msg = "Error processing : '%s'" %(s)
        sys.stderr.write(msg)
        traceback.print_exc(file=sys.stderr)

    
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

def get_reuter_file_paths(dirs = []):
    """
    Get the zip file paths under the directories `dirs`

    >>> paths = get_reuter_file_paths(["/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/", "/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_2/"])
    >>> paths.next()
    '/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/19960824.zip'
    """
    for d in dirs:
        for path in glob("%s/*.zip" %d):
            yield path 

def zip_contents(zip_path):
    """
    Get the file contents in the zip file
    
    Return a generator of the file content

    >>> g = zip_contents("/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/19970101.zip")
    >>> n, c = g.next() # get the content of the next file
    >>> n
    '282799newsML.xml'
    """
    f=ZipFile(zip_path)
    for name in f.namelist():
        yield (name, f.read(name))

def save_content(content, original_file_path, target_directory = "/group/home/puls/Shared/capitalization-recovery/reuters-text/"):
    """
    Save the content somewhere, return the saved path

    >>> save_content("something", "/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/sth.xml", target_directory = "/group/home/puls/Shared/capitalization-recovery/reuters-text/")
    '/group/home/puls/Shared/capitalization-recovery/reuters-text/sth.txt'
    >>> open("/group/home/puls/Shared/capitalization-recovery/reuters-text/sth.txt").read()
    'something'
    """

    original_file_name = os.path.basename(original_file_path)
    file_name = original_file_name.split(".")[0] + ".txt"
    content_path = os.path.join(target_directory, file_name)
    with decode_open(content_path, "w", "utf8") as f:
        f.write(content)
    return content_path
    
def load_reuter_article(content):
    """
    Given the Reuter xml file content, return:

    - title
    - document content

    >>> n, c = zip_contents('/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/19960824.zip').next()
    >>> title, content = load_reuter_article(c)
    >>> title
    u'Harris says hikes dividend 12 pct. [CORRECTED 17:30 GMT, 26/08].'
    >>> content[:9]
    u'Electroni'
    """
    try:
        doc = pq(content)
    except lxml.etree.ParserError:
        raise ValueError("The xml content is invalid")
    
    return unicode(doc.find("headline").text()), unicode(doc.find("text").text())

def prepare_reuter_data(reuter_data_dirs, content_dir):
    """
    Prepare Reuter data in batch.
    
    Extract the title and content in XML files and save the content somewhere,
    meanwhile print the json data arrays
    """
    zippaths = list(get_reuter_file_paths(reuter_data_dirs))[145:]
    for i, zippath in enumerate(zippaths):
        logging.error("%d / %d finished" %(i, len(zippaths)))
        for path_name, xml_content in zip_contents(zippath):
            try:
                t, c = load_reuter_article(xml_content)
            except ValueError:
                logging.error("%s in %s has error" %(path_name, zippath))
                pass
            content_path = save_content(c, path_name, content_dir)
            print json.dumps([content_path, unicode(t).encode("utf8")])

def clean_title_file(path):
    with decode_open(path, "r", "utf8") as f:
        for i,l in enumerate(f):
            if i % 10000 == 0:
                logging.error("%.4f completed", float(i) / 806792)
            obj = json.loads(l)
            words = nltk.word_tokenize(obj[1])
            if is_monocase(words):
                print l, 


if __name__ == "__main__":
    # path = get_file_names()[0]
    import doctest
    doctest.testmod()    

    # prepare_reuter_data(["/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_1/", "/group/home/puls/Shared/capitalization-recovery/RCV1/REUTERS_CORPUS_2/"],
    #                     "/group/home/puls/Shared/capitalization-recovery/reuters-text/")
    # clean_title_file("./reuters.txt")
