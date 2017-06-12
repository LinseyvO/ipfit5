import mailbox
import csv

def more_payloads(message):
	body = ""
	if message.is_multipart():
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		if message.get_content_type() == 'text/plain':
			body += message.get_payload(decode=True)
        return body


writer =csv.writer(open("clean_mail.csv", "wb"))
for message in mailbox.mbox('alice.mbox'):
    body = more_payloads(message)
    writer.writerow([message['subject'], message['from'], message['to'], message['date'], body])

'''writer =csv.writer(open("clean_mailpst4.csv", "wb"))
for message in mailbox.mbox('Outbox'):
    writer.writerow([message['subject'], message['from'], message['to'], message['date']])

writer =csv.writer(open("clean_mailpst5.csv", "wb"))
for message in mailbox.mbox('Sent Items'):
    writer.writerow([message['subject'], message['from'], message['to'], message['date']])

writer =csv.writer(open("clean_mailpst6.csv", "wb"))
for message in mailbox.mbox('Personal Folders'):
    writer.writerow([message['subject'], message['from'], message['to'], message['date']])
'''
