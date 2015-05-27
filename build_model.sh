#! /bin/bash

./run_training_size_experiment.sh 1+2+3+4+5  cap 30000 /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_cap/30000/train.txt /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_cap/30000/test.txt

./run_training_size_experiment.sh 1+2+3+4+5  lower 30000 /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_lower/30000/train.txt /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_lower/30000/test.txt

./run_training_size_experiment.sh 1+2+3+4+5  upper 30000 /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_upper/30000/train.txt /cs/taatto/home/hxiao/capitalization-recovery/corpus/news_title_upper/30000/test.txt
