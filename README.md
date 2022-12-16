# Slackdump2Html

This script transforms a JSON file created by [slackdump](https://github.com/rusq/slackdump) to a static HTML file.

A lot of companies that switch from Slack to another communication tool lose a lot of implicit knowledge that has been gathered potentially over years.
In order to preserve this knowledge in a human-readable and easily searchable way, we have created this script.
The output file is a self-contained html document that can easily be uploaded to any web or file server or shared with specific people in your organization.

Please be aware that this script does not support file attachments.

# Setup

## Slackdump

Before being able to convert the JSON file, you need to download it via slackdump.<br>
Download an executable version of slackdump and put it in the root directory of your clone of this repo.<br> 
Follow the [slackdump User Guide](https://github.com/rusq/slackdump/blob/master/doc/README.rst) to install and set up the tool and provide your authentication tokens.

To get your channel ids, use this command
```
./export-channels.sh
-- or
./slackdump -list-channels > data/channels.txt
```

You'll also need a user dump
```
./export-users.sh
-- or
./slackdump -list-users > data/users.txt
```

You'll also need an emoji dump
```
./export-emojis.sh
-- or
./slackdump -emoji -base data/emojis
```

## Python

In order to run this script, you need to have Python installed. If you don't have it, please [download](https://www.python.org/downloads/) the latest version.
There are libraries needed. See the Pipfile for what's needed.
```
pipenv install
```

# Usage

## Automatically

Fetch the ID of the channel (e.g. C03HQM5DE) you want to export from the data/channels.txt file and run
```
./dump-and-convert.sh
```
Provide the channel ID when it asks for it. You'll find your output file in out/<channel-name>.html.

## Manually

You'll need to dump the channel you want to convert via slackdump.
Use the data/channels.txt file to get the ID of your channel (e.g. C03HQM5DE) and use slackdump to dump the channel to a json.
Grab a coffee, this might take a while.
```
./slackdump <your-channel-id>
Example:
./slackdump C03HQM5DE
```

Convert your slackdump to a html file with this command.
```
python slackdump2html.py <path-to-your-export-file>
Example:
python slackdump2html.py C03HQM5DE.json
```
You'll find your output file in out/<channel-name>.html.

# Known issues
* Emojis
  * Thy python emoji package does not consider markup languages and replaces emojis in HTML links. This might break some of your links.
  * Not all emojis can be replaced correctly.
  * Not all image types are supported as custom emojis.
* File attachments
  * File attachments are not supported at all.