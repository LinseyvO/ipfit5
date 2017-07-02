import mailbox
import csv
import os
import sys
from email.header import decode_header
from pandas import read_csv
import sqlite3

def getbody(message): # hiet wordt de body uit de mail gehaald
    body = None #variabele body wordt aangemaakt
    if message.is_multipart(): # deze returned true wanneer de message zijn payload sub-objecten zijn.
        for part in message.walk(): # walk itereert over alle delen en subdelen in de objecttree
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain': # deze wordt uitgevoerd wanneer de message een string is.
                        body = subpart.get_payload(decode=True) # returned de payload welke bestaat uit message objecten als multipart true is en een string als multipart false is
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body # wanneer deze functie aangeroepen wordt returned deze de body waarde

writer =csv.writer(open("./mail/clean_mail.csv", "wb")) # er wordt een csv bestand geopend genaamd 'clean_mail.csv'

dirt = './mail/' # de variabele dirt wordt gelijk gemaakt aan het opgegeven pad
for root,dirs, filenames in os.walk(dirt): # geitereert over de dirt folder
    for f in filenames: 
        if f.endswith('.mbox'): # als de f(file) in de opgegeven folder op .mbox eindigt 
            mboxfile = f # wordt de variabele mboxfile hieraan gelijk gemaakt
            print (f) # f wordt geprint 

            ff = './mail/' + mboxfile # ff wordt gelijk gemaakt aan het pad + de gevonden mboxfiles

            for message in mailbox.mbox(ff): # nu wordt door de mboxfiles gelopen in het eerder opgegeven pad
                body = getbody(message) # de getbody functie wordt hier aangeroepen
                writer.writerow([message['subject'], message['from'], message['to'], message['date'], body]) #uit het mbox bestand worden nu de gevonden subjects, from, to, date en body naar de eerder aangemaakte csv weggeschreven
