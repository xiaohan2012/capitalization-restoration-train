# Usage

## Train the model

### Preparing data

```
./make_data.sh
```

### Train models

Either run `./all_feature_experiments.sh` or `./all_training_size_experiments.sh` to prepare the scripts.

Then `./distribute.sh training_size_experiments_commands.sh|feature_experiments_commands.sh` to distribute it across ukko cluster

To change the machines to deploy upon, change `servers.lst` file.

### Model path

They lie under `/cs/taatto/home/hxiao/capitalization-recovery/result/`.

For example: for lower case, training sie 3000, the model is

`/cs/taatto/home/hxiao/capitalization-recovery/result/training_size/lower/30000/`

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



