#! /bin/bash

doc_ids_path=data/tmp/2015-08-18/trainable_doc_ids.txt
ok_path=/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format/
mal_path=/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format-rule-based

time python rule_based.py ${doc_ids_path}  ${ok_path} ${mal_path}
