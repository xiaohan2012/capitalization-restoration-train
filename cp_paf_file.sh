#! /bin/bash

src_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
target_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-rule-based'

id_file=$1

if [ -z $id_file ]; then
	echo "id_file should be given"
	exit -1
fi

while read id; do
	cp "${src_corpus_dir}/${id}.paf" "${target_corpus_dir}/"
done < $id_file
