#!/bin/bash
rm data/users.txt -f
mkdir data -p
./slackdump -list-users > data/users.txt