#! /bin/bash

DATA_ROOT="/cs/taatto/home/hxiao/capitalization-recovery/result/feature"

modes=(upper lower cap)
features=1+2+3+4+5+6
size=30000

for mode in "${modes[@]}"
do
	echo "mode: $mode"
	echo "size: $size"
	cp $DATA_ROOT/$mode/$features/model models/${mode}_model.bin
done
