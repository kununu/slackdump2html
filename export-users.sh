#!/bin/bash
rm -f data/users.txt
mkdir -p data
./slackdump -list-users > data/users.txt