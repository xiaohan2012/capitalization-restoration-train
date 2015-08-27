#! /bin/bash

#./run_feature_experiment 1+2+3 upper train_path test_path 

feature_ids=1+3+4+6
train_path="/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/train.txt"
test_path="/cs/taatto/home/hxiao/capitalization-recovery/data/puls-100k/test.txt"

result_dir="/cs/taatto/home/hxiao/capitalization-recovery/result/puls-100k"


if [ ! -d $result_dir ]; then
	mkdir -p $result_dir
fi

cd ~/code/capitalization_train/

# cat $train_path | python crfsuite-0.12/example/chunking.py $feature_ids  > $result_dir/train.crfsuite.txt

./crfsuite-0.12/bin/crfsuite learn -g10 -x -l $result_dir/train.crfsuite.txt > $result_dir/cross_validation.txt

# ./crfsuite-0.12/bin/crfsuite learn -m $result_dir/model $result_dir/train.crfsuite.txt
