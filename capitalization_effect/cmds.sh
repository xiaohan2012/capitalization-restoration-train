#! /bin/bash

echo "python chunk.py upper > results/chunk_upper.txt"
python chunk.py upper > results/chunk_upper.txt

echo "python chunk.py lower > results/chunk_lower.txt"
python chunk.py lower > results/chunk_lower.txt

echo "python chunk.py > results/chunk.txt"
python chunk.py > results/chunk.txt
