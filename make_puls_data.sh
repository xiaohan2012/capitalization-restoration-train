#! /bin/bash

train_path=/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/train.txt
test_path=/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/test.txt

python make_data_puls.py 0 100000 > $train_path
python make_data_puls.py 100001  > $test_path
