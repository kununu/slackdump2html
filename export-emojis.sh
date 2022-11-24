#!/bin/bash
rm data/emojis -f -r
mkdir data/emojis -p
./slackdump -emoji -base data/emojis