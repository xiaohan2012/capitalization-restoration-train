># Usage

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


## Producing new data set for CRF classifier

Use the working script: `new_data_pipeline.sh`. Basically, it does the above.

Or do the following step by step by hand(not recommended)

1. `python print_filenames_and_titles.py`: get the file paths and news titles that accords to our requirement(non-monocase title and non-empty article body)
2. `python copy_puls_file_to_local.py`: copy the files somewhere writable&accessible
3. `python extract_doc_ids.py`: save the ids of documents to be used
4. `puls-core-process-document.sh`: using PULS to preprocess the documents. This will generate the `.auxil` files
5. `process_and_save_capitalized_headlines.py`: save the malformed headlines somewhere
6. `make_data_puls.py`: extract the features for CRF classifier to use
7. `train_puls_model.sh`: train the model

## Producing new data set for rule-based classifier

The process is divided into two parts: one part is shared with the data creation process for CRF classifier(step 1 to 5).

The other is outputing the labels for the rule-based classifier to use.

Run `make_rule_based_corpus.sh`
