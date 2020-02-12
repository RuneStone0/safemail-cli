# CLI Tool for Safemail
This is a CLI tool for Safemail by Deltagon (https://www.deltagon.com/). The intention of this tool is to speed up the process of sending multiple emails through the Safemail tool.

# Setup
1. Open `smailer.py` and update the config section to match your end-point
2. Setup local environment
    a. `virtualenv venv`
    b. `pip install -r requirements.txt`
3. Run program: `python smailer.py`

# Example
```
python smailer.py --help
usage: smailer.py [-h] [--key] [--subject] [--message] [--to] [--url] [--attach [file.pdf [file.pdf ...]]]
                  [--send]

Safemail CLI.

optional arguments:
  -h, --help            show this help message and exit
  --key                 Safemail KEY
  --subject             Email Subject
  --message             Email Message
  --to                  Email Recipients. Format: [email].[phone].s,[email].[phone].s
  --url                 Safemail URL endpoint. Example: https://safemail.company.com/. Note, the URL must end
                        with a trailing / (forward slash)
  --attach [file.pdf [file.pdf ...]]
                        One or more files to attach
  --send                When set, the email will be sent. If not, a preview will be shown.
```