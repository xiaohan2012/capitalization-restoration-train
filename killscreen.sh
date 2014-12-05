#! /bin/bash
screen -ls | grep '[0-9]\.' | cut -d. -f1 | awk '{print $1}' | xargs kill
