#! /bin/bash
echo 1
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 > tmp/monocase/1/test-e.crfsuite.txt
echo 2
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 > tmp/monocase/2/test-e.crfsuite.txt
echo 3
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 3 > tmp/monocase/3/test-e.crfsuite.txt
echo 1 2
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 2 > tmp/monocase/1+2/test-e.crfsuite.txt
echo 1 3
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 1 3 > tmp/monocase/1+3/test-e.crfsuite.txt
echo 2 3
date
echo data/monocase/trainable/reuters-j
cat data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-j.crfsuite.txt
cat data/monocase/trainable/reuters-j | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-j.crfsuite.txt
date
echo data/monocase/trainable/reuters-h
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-h.crfsuite.txt
cat data/monocase/trainable/reuters-h | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-h.crfsuite.txt
date
echo data/monocase/trainable/reuters-i
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-i.crfsuite.txt
cat data/monocase/trainable/reuters-i | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-i.crfsuite.txt
date
echo data/monocase/trainable/reuters-b
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-b.crfsuite.txt
cat data/monocase/trainable/reuters-b | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-b.crfsuite.txt
date
echo data/monocase/trainable/reuters-c
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-c.crfsuite.txt
cat data/monocase/trainable/reuters-c | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-c.crfsuite.txt
date
echo data/monocase/trainable/reuters-a
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-a.crfsuite.txt
cat data/monocase/trainable/reuters-a | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-a.crfsuite.txt
date
echo data/monocase/trainable/reuters-f
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-f.crfsuite.txt
cat data/monocase/trainable/reuters-f | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-f.crfsuite.txt
date
echo data/monocase/trainable/reuters-g
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-d data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-g.crfsuite.txt
cat data/monocase/trainable/reuters-g | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-g.crfsuite.txt
date
echo data/monocase/trainable/reuters-d
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-d.crfsuite.txt
cat data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-d.crfsuite.txt
date
echo data/monocase/trainable/reuters-e
cat data/monocase/trainable/reuters-j data/monocase/trainable/reuters-h data/monocase/trainable/reuters-i data/monocase/trainable/reuters-b data/monocase/trainable/reuters-c data/monocase/trainable/reuters-a data/monocase/trainable/reuters-f data/monocase/trainable/reuters-g data/monocase/trainable/reuters-d | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/train-e.crfsuite.txt
cat data/monocase/trainable/reuters-e | python crfsuite-0.12/example/chunking.py 2 3 > tmp/monocase/2+3/test-e.crfsuite.txt
