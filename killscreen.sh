#! /bin/bash

taskname=$1
if [ -z "$taskname" ]
then
	echo "Task name should be specified"
	exit
fi

screen -ls | grep "[0-9]\.$taskname" | cut -d. -f1 | awk '{print $1}' | xargs kill
