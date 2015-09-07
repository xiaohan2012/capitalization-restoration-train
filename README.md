
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

The other is outputing the labels in separate files for the rule-based classifier to use.

Run `make_rule_based_corpus.sh`


## Evaluation
### CRF classifier evaluation

Refer to the comments in `train_puls_model.sh` and comment/uncomment certain lines to do that.

Itermediate performance statitics(as they will be processed later) will be saved in target paths as specified in that script.


### Rule-based classifier evaluation

Do the following:

- Change the variables in `puls-rule-based-parallel.sh` if you'd like to
- Run `puls-rule-based-parallel.sh` to use the IE rule-based capitalization recovery tool to process the evaluation data
- Go to the directory specified by `$result_dir` variable in the `puls-rule-based-parallel.sh` and concatenate all the result files (starting with `id_`) into a whole result file
- Run `python evaluate.py` to print the result matrix, where rows are the statistics for each label and columns are `number of match`, `number of predictions y model` and `number of lables in reality`

### Post processing

Both evaluation scripts print out itermediate result(like number of correct predictions support) for the final scores. You need to run replace the data in `calc_cv_result.py` according to the comment in the script and run it.



## Printing error example

For CRF classiier, `pred_err.py` will print out the error examples as well as confusion matrix

    > # Example: python pred_err.py ${model_path} ${test_sentence_path} ${test_sentence_feature_path}
	> DATA_ROOT=/cs/taatto/home/hxiao/capitalization-recovery
    > python pred_err.py --model ${DATA_ROOT}/result/feature/cap/1+2+3+4+5+6/model --sent_path ${DATA_ROOT}/corpus/news_title_cap/30000/test.txt --crfsuite_path ${DATA_ROOT}/result/feature/cap/1+2+3+4+5+6/test.crfsuite.txt

For rule-based classifier, `evaluate.py` will do the same role. Note, you need to set `print_errors=True` when  calling `eval_rule_based` in the `evaluate.py` script.

## Trainable document Id path

Documents are filtered by whether their title is trainable(correctly-capitalized) and whether they contain non-empty body, the list of document ids is saved under `data/tmp/2015-08-18/filtered_trainable_doc_ids.txt`


## TODO
- Add more features to handle mixed-case words, for example: TSX-Venture, or split the word by the hyphen
- In capitalized titles(more information is preserved), some words are already all-uppercase/mixed-cased. Dictionary feature does not take into account mixed case words.
- Spelling/morphology, funds = fund + s
- POS tag for capitalized words seems to tend to be NNP. Maybe lowercase the sentence and capitalize it?
