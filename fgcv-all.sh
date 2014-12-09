#! /bin/bash

while read line
do
    server=$line
    echo "Deploying $server.."
    script_path="fgcv_scripts/$server.sh"
    ssh $server.hpc.cs.helsinki.fi 'bash -s'  < $script_path
done < fgcv_servers.txt