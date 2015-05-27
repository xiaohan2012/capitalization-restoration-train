#! /bin/bash
function get_item_accuracy() {
	echo $(cat $1 | grep "Item accuracy" | grep -o -E "0.[0-9]{4}")
}

function get_f1_score() {
	echo $(cat $1 | grep "Macro-average precision, recall, F1" | grep -o -E "0.[0-9]{4}")
}

for f in $(find /cs/taatto/home/hxiao/capitalization-recovery/result/training_size -name result.txt); do
	size=$(basename $(dirname $f))
	mode=$(basename $(dirname $(dirname $f)))
	accuracy=$(get_item_accuracy $f)
	f1_score=$(get_f1_score $f)
	echo -e "$mode $size $accuracy $f1_score"
done

