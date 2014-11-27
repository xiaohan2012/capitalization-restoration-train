#! /bin/bash

echo $1

for i in $(ls $1/*.zip); do
	unzip $i -d $1
done
