# Slackdump2Html

This script transforms a JSON file created by [slackdump](https://github.com/rusq/slackdump) to a static HTML file.

A lot of companies that switch from Slack to another communication tool lose a lot of implicit knowledge that has been gathered potentially over years.
To preserve this knowledge in a human-readable and easily searchable way, we have created this script.
The output file is a self-contained HTML document that can easily be uploaded to any web or file server or shared with specific people in your organization.

Please be aware that this script does not support file attachments.

## Setup

### Slackdump

Before being able to convert the JSON file, you need to download it via `slackdump`.

Download an executable version of `slackdump` and put it in the root directory of your clone of this repo.

Follow the [slackdump User Guide](https://github.com/rusq/slackdump/blob/master/doc/README.rst) to install and set up the tool and provide your authentication tokens.

To get your channel ids, use this command

```bash
./export-channels.sh
-- or
./slackdump -list-channels > data/channels.txt
```

You'll also need a user dump

```bash
./export-users.sh
-- or
./slackdump -list-users > data/users.txt
```

You'll also need an emoji dump

```bash
./export-emojis.sh
-- or
./slackdump -emoji -base data/emojis
```

### Python

To run this script, you need to have Python installed. If you don't have it, please [download](https://www.python.org/downloads/) the latest version.

There are libraries needed. See the Pipfile for what's needed.

```bash
pipenv install
```

## Usage

### Automatically

Fetch the ID of the channel (e.g. `C03HQM5DE`) you want to export from the `data/channels.txt` file and run

```bash
./dump-and-convert.sh
```

Provide the channel ID when it asks for it. You'll find your output file in `out/<channel-name>.html`.

### Manually

You'll need to dump the channel you want to convert via `slackdump`.
Use the `data/channels.txt` file to get the ID of your channel (e.g. `C03HQM5DE`) and use `slackdump` to dump the channel to a JSON file.
Grab a coffee, this might take a while.

```bash
./slackdump -download -base data/messages <your-channel-id>
Example:
./slackdump -download -base data/messages C03HQM5DE
```

Convert your `slackdump` to an HTML file with this command.

```bash
python slackdump2html.py <path-to-your-export-file> <path-to-your-image-files> 
Example:
python slackdump2html.py data/messages/C03HQM5DE.json  data/messages/C03HQM5DE
```

You'll find your output file in `out/<channel-name>.html`.

## Known issues

* Emojis:
  * Thy python emoji package does not consider markup languages and replaces emojis in HTML links. This might break some of your links.
  * Not all emojis can be replaced correctly.
  * Not all image types are supported as custom emojis.

* File attachments:
  * File attachments are not supported at all.

* Code blocks:
  * Some formatting in code blocks is broken.

* EZ-Login 3000 might not work in Linux:
  * Define a `.env` file with a `SLACK_TOKEN=xoxc-...` and `COOKIE=./app.slack.com_cookies.txt` variable.
  * Or pass the via command line arguments `-t xoxc-... -cookie ./app.slack.com_cookies.txt`
