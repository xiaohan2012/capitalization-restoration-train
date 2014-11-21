"""
Baseline capitalization restorer

It checks whether the word appears as capitalized in the document or not
"""
import nltk
from data import (appear_capitalized_indoc_label,
                  get_label)

def normalize_title(title = "", words = [], **kwargs):
    if title:
        words = nltk.word_tokenize(title)

    head = words[0][0].upper() + words[0][1:]
    tail = words[1:]

    doc = kwargs["doc"]
    return [head] + [w
                     if ("IN_DOC_CAP" == appear_capitalized_indoc_label(w, doc) )
                     else
                     w[0].lower() + w[1:]
                     for w in tail]


    
