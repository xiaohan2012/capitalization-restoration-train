#! /bin/bash

# ops=(lower upper cap)
ops=(cap)
# sizes=(5000 10000 15000 20000 25000 30000)

# ops=(upper)
sizes=(30000)

for size in "${sizes[@]}"
do
	echo "size: $size"
	for op in "${ops[@]}"
	do
		echo "op: $op"
		if [ ! -d corpus/news_title_$op/$size/ ]; then
			mkdir -p corpus/news_title_$op/$size/
		fi
		home_train_path=corpus/news_title_$op/$size/train.txt
		home_test_path=corpus/news_title_$op/$size/test.txt
		dest_train_path=/cs/taatto/home/hxiao/capitalization-recovery/$home_train_path
		dest_test_path=/cs/taatto/home/hxiao/capitalization-recovery/$home_test_path

		echo -e "Output to: ${dest_train_path}\n${dest_test}"

		python data.py fnames_and_titles.txt $op 0 $size > $home_train_path
		python data.py fnames_and_titles.txt $op 30001  > $home_test_path

		cp $home_train_path $dest_train_path
		cp $home_test_path $dest_test_path
	done
done
