#! /bin/bash

ops=(lower upper cap)
sizes=(5000 10000 15000 20000 25000 30000)

for size in "${sizes[@]}"
do
	echo "size: $size"
	for op in "${ops[@]}"
	do
		echo "op: $op"
		if [ ! -d corpus/news_title_$op/$size/ ]; then
			mkdir -p corpus/news_title_$op/$size/
		fi
		python data.py fnames_and_titles.txt cap 0 $size > corpus/news_title_$op/$size/train.txt
		python data.py fnames_and_titles.txt cap 30001  > corpus/news_title_$op/$size/test.txt
	done
done
