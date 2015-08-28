#!/bin/bash

doc_ids_path="data/tmp/2015-08-18/trainable_doc_ids.txt"
result_dir="/cs/taatto/home/hxiao/capitalization-recovery/result/puls-100k/rule-based"
puls_task_chunks=16

echo "puls-rule-based"
split -n ${puls_task_chunks} ${doc_ids_path} id_
rm data/docids/id_*
mv id_* data/docids

cd data/docids
ids=$(ls .)
echo ${ids}
echo "In '$(pwd)'"

parallel ../../puls-rule-based.sh "{}" '1>' "${result_dir}/{}.txt" :::  ${ids}
