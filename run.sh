#! /bin/sh

cat train.txt | python crfsuite-0.12/example/chunking.py > train.crfsuite.txt
cat test.txt | python crfsuite-0.12/example/chunking.py > test.crfsuite.txt

./crfsuite-0.12/bin/crfsuite learn -m cap.model train.crfsuite.txt
./crfsuite-0.12/bin/crfsuite tag -qt -m cap.model test.crfsuite.txt
