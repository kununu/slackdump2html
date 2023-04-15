#!/bin/bash
rm -f data/channels.txt
mkdir -p data
./slackdump -list-channels > data/channels.txt