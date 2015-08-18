#! /bin/bash

doc_ids_path=data/tmp/2015-08-18/doc_ids.txt
train_path=/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/train.txt
test_path=/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/test.txt

time python make_puls_data.py ${doc_ids_path}  0 > $train_path
# time python make_data_puls.py ${doc_ids_path} 100001  > $test_path
