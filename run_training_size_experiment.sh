#! /bin/bash
#./run_feature_experiment 1+2+3 upper size train_path test_path 

feature_ids=$1
mode=$2
size=$3
train_path=$4
test_path=$5

my_dir="/cs/taatto/home/hxiao/capitalization-recovery/result/training_size/$mode/$size"

echo "At $my_dir"

if [ ! -d $my_dir ]; then
	mkdir -p $my_dir
fi

cd ~/code/capitalization-restoring/

cat $train_path | python crfsuite-0.12/example/chunking.py $feature_ids > $my_dir/train.crfsuite.txt
cat $test_path | python crfsuite-0.12/example/chunking.py $feature_ids > $my_dir/test.crfsuite.txt

./crfsuite-0.12/bin/crfsuite learn -m $my_dir/model $my_dir/train.crfsuite.txt

./crfsuite-0.12/bin/crfsuite tag -qt -m $my_dir/model $my_dir/test.crfsuite.txt > $my_dir/result.txt

# remove train data to save space
rm $my_dir/train.crfsuite.txt 
# rm $my_dir/model
# rm $my_dir/test.crfsuite.txt
