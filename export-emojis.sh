#!/bin/bash
rm -f -r data/emojis
mkdir -p data/emojis
./slackdump -emoji -base data/emojis