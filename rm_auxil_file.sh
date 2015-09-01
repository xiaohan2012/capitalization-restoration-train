#! /bin/bash

src_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
target_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'

id_file=$1

if [ -z $id_file ]; then
	echo "id_file should be given"
	exit -1
fi

while read id; do
	# rm "${src_corpus_dir}/${id}.auxil"
	rm "${target_corpus_dir}/${id}.auxil"
	rm "${target_corpus_dir}/${id}.paf"
done < $id_file
