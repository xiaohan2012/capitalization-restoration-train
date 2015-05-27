# Usage

## Train the model

## Python interface

```
>>> from cap_restore import restore
>>> restore('some text')
```

## Command-line tool

Run 

```
>>> python cap_restore.py -h
```

## TODO
- Add more features to handle mixed-case words, for example: TSX-Venture, or split the word by the hyphen
- In capitalized titles(more information is preserved), some words are already all-uppercase/mixed-cased. Dictionary feature does not take into account mixed case words.
- Spelling/morphology, funds = fund + s
- POS tag for capitalized words seems to tend to be NNP. Maybe lowercase the sentence and capitalize it?
- 



