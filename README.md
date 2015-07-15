# Usage

## Train the model

### Preparing data


    ./make_data.sh


Note:

Everytime you want to add more features, you only need to run this script once.

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

## Error analysis utility

The `pred_err.py` util will print out the error examples as well as confusion matrix

    > # Example: python pred_err.py ${model_path} ${test_sentence_path} ${test_sentence_feature_path}
	> DATA_ROOT=/cs/taatto/home/hxiao/capitalization-recovery
    > python pred_err.py --model ${DATA_ROOT}/result/feature/cap/1+2+3+4+5+6/model --sent_path ${DATA_ROOT}/corpus/news_title_cap/30000/test.txt --crfsuite_path ${DATA_ROOT}/result/feature/cap/1+2+3+4+5+6/test.crfsuite.txt

## TODO
- Add more features to handle mixed-case words, for example: TSX-Venture, or split the word by the hyphen
- In capitalized titles(more information is preserved), some words are already all-uppercase/mixed-cased. Dictionary feature does not take into account mixed case words.
- Spelling/morphology, funds = fund + s
- POS tag for capitalized words seems to tend to be NNP. Maybe lowercase the sentence and capitalize it?
- 



