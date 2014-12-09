#! /bin/bash

while read line
do
    server=$line
    echo "Deploying cv to $server.."
    script_path="cv_scripts/$server.sh"
    ssh $server.hpc.cs.helsinki.fi 'bash -s'  < $script_path
done < servers.txt
