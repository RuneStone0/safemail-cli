import sys
import requests
import re
import argparse


##### CONFIG ######
config_safemail_url = "https://safemail.company.com/" # REMEBER trailing slash
config_key = "xxxxxxxx" # Unique ID for sending mails 
config_subject = "HOW TO TIP?"
config_message = """
GO TO ATM, CASH OUT, TIP TIP TIP!!
"""
config_signature = """
--
Stan
+00 11 22 33 44
"""
config_recipients = "stan@staninvegas.com.001122334.4s" # Format: [email].[phone].s,[email].[phone].s
###################

def SaveResponse(data, outfile):
	response = data.encode("utf-8")
	file = open(outfile, "wb") 
	file.write(response) 
	file.close()
	print("Writing data to: " + outfile)

def PrintSummary(payload):
	print("================ MESSAGE ===============")
	print("FROM:\t\t" + payload["sender"])
	print("TO:\t\t" + payload["recipient"])
	print("SUBJECT:\t" + payload["subject"])
	print("MESSAGE:" + payload["message"])
	print("SIGNATURE:" + payload["signature"])
	if opts.attach: 
		print("ATTACHMENT(S):")
		for filepath in opts.attach: print(filepath)
	else:
		print("ATTACHMENT(S): No attachments.")
	print("========================================")

def AttachFile(payload):
	file = None
	if opts.attach:
		for filepath in opts.attach:
			try:
				file = {'upfile': open(filepath,'rb')}
			except:
				print("Invalid file path(s).")
				sys.exit()
			payload["formattach"] = "Attach" # We tell safemail that we're uploading an attachment
			response = s.post(config_safemail_url+"index.cgi", data=payload, files=file)
			payload.pop("formattach") # Remove instruction that we're uploading files
			#SaveResponse(response.text, "s_attach.html") # Debugging only

def SendMessage(payload):
	payload["formsubmit"] = "Send" # We tell safemail, to send the message
	response = s.post(config_safemail_url+"index.cgi", data=payload)
	if "Message sent successfully" in response.text:
		PrintSummary(payload)
		print("Message sent successfully")
	else:
		print("ERROR: Something went wrong!!")
	#SaveResponse(response.text, "s_send.html") # Debugging only

help_text = "Safemail CLI."
parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("--key", default=config_key, metavar="", type=str, required=False, help="Safemail KEY")
parser.add_argument("--subject", default=config_subject, metavar="", type=str, required=False, help="Email Subject")
parser.add_argument("--message", default=config_message, metavar="", type=str, required=False, help="Email Message")
parser.add_argument("--to", default=config_recipients, metavar="", type=str, required=False, help="Email Recipients. Format: [email].[phone].s,[email].[phone].s")
parser.add_argument("--url", default=config_safemail_url, metavar="", type=str, required=False, help="Safemail URL endpoint. Example: https://safemail.company.com/. Note, the URL must end with a trailing / (forward slash)")
parser.add_argument("--attach", type=str, required=False, metavar="file.pdf", nargs='*', help="One or more files to attach")
parser.add_argument("--send", action='store_true', help="When set, the email will be sent. If not, a preview will be shown.")
opts = parser.parse_args()

# Login
try:
	s = requests.session()
	response = s.get(config_safemail_url+"index.cgi?"+opts.key)
	sender = re.search(r'(?:VALUE=")(.*&#64;.*)(?:" class)', response.text).group(1)
	regurl = re.search(r'(?:regurl" VALUE=")(.*)(?:">)', response.text).group(1)
	id1 = re.search(r'(?:id1" VALUE=")(.*)(?:">)', response.text).group(1)
	session = re.search(r'(?:session" VALUE=")(.*)(?:">)', response.text).group(1)
	lang = re.search(r'(?:lang" VALUE=")(.*)(?:">)', response.text).group(1)
	recipients = opts.to
except:
	print("Authentication failed. Verify your safemail KEY")
	sys.exit()


# Set recipient(s)
payload = {
  "sender": sender.replace("&#64;", "@"),
  "recipient": opts.to,
  "id1": id1,
  "session": session,
  "regurl": regurl,
  "lang": lang,
  "chatset": "utf-8",
  "signature": config_signature,
  "subject": opts.subject,
  "message": opts.message,
}

# If --send is found
if opts.send:
	AttachFile(payload)
	SendMessage(payload)

# Show message preview when --send it not set
else:
	PrintSummary(payload)
	print("Use --send to deliver the message.")
