#! /bin/bash

src_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
target_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'

id_file=$1

if [ -z $id_file ]; then
	echo "id_file should be given"
	exit -1
fi

src_count=0
target_count=0

while read id; do
	src_path="${src_corpus_dir}/${id}.auxil"
	if [ -f ${src_path} ] && [ "`ls -l ${src_path} | awk '{print $5}'`" != "0" ]; then
		src_count=$((src_count + 1))
	fi

	target_path="${target_corpus_dir}/${id}.auxil"
	if [ -f  "${target_corpus_dir}/${id}.auxil" ] && [ "`ls -l ${target_path} | awk '{print $5}'`" != "0" ]; then
		target_count=$((target_count + 1))
	fi
done < $id_file

echo "src_count: ${src_count}"
echo "target_count: ${target_count}"
