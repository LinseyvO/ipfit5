import mailbox
import csv
import os
import sys
from email.header import decode_header
from pandas import read_csv
import sqlite3

def getbody(message): # haal de body uit het e-mail bestand
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

writer =csv.writer(open("clean_mail.csv", "wb")) # er wordt een csv bestand aangemaakt en er kan nu data naar worden geschreven

dirt = './MAIL/' # er wordt een variabel aangemaakt waarin het pad wordt gezet
for root,dirs, filenames in os.walk(dirt): # deze loop loopt door opgegeven map heen en zoekt naar bestanden die eindigen met de extensie '.mbox'
    for f in filenames:
        if f.endswith('.mbox'):
            mboxfile = f # deze variabele wordt gelijk gemaakt aan de naam van het gevonden bestand dat eindigt op '.mbox'
            print (f) # voor controle wordt de naam van het gevonden mbox bestand naar de terminal geprint

            for message in mailbox.mbox(mboxfile): # hier wordt de data naar het csv bestand weggeschreven
                body = getbody(message)
                writer.writerow([message['subject'], message['from'], message['to'], message['date'], body])











