#! /bin/bash

source ~/.bashrc

cmd_file=$1

if [ -z "$cmd_file" ]; then
	echo "cmd file should be given"
	exit -1
fi

servers=$(<servers.lst)
echo "SERVERS TO DEPLOY: "
echo $servers

export JAVA_HOME=/cs/fs/home/hxiao/software/jre1.8.0_31

cat $cmd_file | parallel  --progress -S  $servers  --workdir . --jobs 1 


