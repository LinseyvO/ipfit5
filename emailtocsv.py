import mailbox
import csv
import os
import sys
from email.header import decode_header
from pandas import read_csv
import sqlite3


'''def more_payloads(message):
	body = ""
	if message.is_multipart():
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		if message.get_content_type() == 'text/plain':
			body += message.get_payload(decode=True)
        return body
'''
def getbody(message): #getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body

writer =csv.writer(open("clean_mail.csv", "wb"))

dirt = './MAIL/'
for root,dirs, filenames in os.walk(dirt):
    for f in filenames:
        if f.endswith('.mbox'):
            mboxfile = f
            print (f)

            for message in mailbox.mbox(mboxfile):
                body = getbody(message)
                writer.writerow([message['subject'], message['from'], message['to'], message['date'], body])











