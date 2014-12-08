#! /bin/bash

while read line
do
    server=$line
    echo "Stopping $server.."
    ssh $server.hpc.cs.helsinki.fi 'bash -s' < killscreen.sh
done < $1



