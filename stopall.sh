#! /bin/bash

if [ -z "$1" ]
then
	echo "Server list should be specified"
	exit
fi

if [ -z "$2" ]
then
	echo "Task name should be specified"
	exit
fi

while read line
do
    server=$line
    echo "Stopping $server.."
    ssh $server.hpc.cs.helsinki.fi 'bash -s' < killscreen.sh "$2"
done < $1


