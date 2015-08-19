#!/bin/bash

now=$(date +%Y-%m-%d)

# now="2015-08-18"

mkdir -p data/tmp/${now}

filenames_and_titles_path="data/tmp/${now}/fnames_and_titles.txt"
doc_ids_path="data/tmp/${now}/doc_ids.txt"

src_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format'
target_corpus_dir='/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-capitalized'

puls_task_chunks=16

echo "printing filenames to ${filenames_and_titles_path}"
python print_filenames_and_titles.py > ${filenames_and_titles_path}

echo "copy corpus to local directory ${target_corpus_dir}"
python copy_puls_file_to_local.py ${filenames_and_titles_path} ${src_corpus_dir}

echo 'extract the ids'
python extract_doc_ids.py ${filenames_and_titles_path} > ${doc_ids_path}

echo "puls-process"
split -n ${puls_task_chunks} ${doc_ids_path} id_
rm data/docids/id_*
mv id_* data/docids

cd data/docids
ids=$(ls .)
echo ${ids}
echo "In '$(pwd)'"

parallel ../../puls-core-process-document.sh :::  ${ids}

cd ../..

echo "In '$(pwd)'"

echo "extract and capitalize titles"
python process_and_save_capitalized_headlines.py  ${doc_ids_path} ${src_corpus_dir} ${target_corpus_dir}

echo "processing cap headlines"
ids=$(ls .)
echo ${ids}
parallel ../../puls-core-process-document.sh :::  ${ids}
cd ../..

# echo "making feature data"
# ./make_puls_data.sh

# echo "output the labels"
python rule_based.py ${trainable_doc_ids} ${src_corpus_dir} ${target_corpus_dir}
