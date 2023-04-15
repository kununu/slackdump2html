#!/bin/bash
echo "What channel should be exported?"
echo "Please enter the internal channel ID of slack (eg. GSE6ZQDHT)"
read -r channel
./slackdump "$channel"
python slackdump2html.py "$channel.json"
read -p "Press Enter to finish" </dev/tty
