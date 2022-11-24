#!/bin/bash
rm data/channels.txt -f
mkdir data -p
./slackdump -list-channels > data/channels.txt