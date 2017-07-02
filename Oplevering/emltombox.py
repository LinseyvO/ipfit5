#!/usr/bin/env python
'''
dit script convert een hele folder met eml bestanden of een enkel eml bestand naar een mbox file

als input wordt dus een folder en een enkele file geaccepteerd

als output.mbox nog niet bestaat wordt deze aangemaakt. Als hij bestaat,
Wordt er data aan toegevoegd. 
'''


import os
import sys
import mailbox

global debug
debug = True


def main(arguments):
    infile_name = ('./mail') # de variabel wordt gelijk gemaakt aan de huidige map
    dest_name = ('./mail/outbox.mbox') # de variabel wordt een gelijk gemaakt aan een bestand in het opgegeven pad

    if debug:
        print "Input is:  " + infile_name #het script geeft feedback
        print "Output is: " + dest_name #het script geeft feedback

    if not os.path.exists('./mail'): # er wordt gekeken of het opgegeven pad bestaat
        os.makedir('./mail') # zoniet wordt deze aangemaakt

    dest_mbox = mailbox.mbox(dest_name, create=True)  # als de destinatie niet bestaat wordt deze aangemaakt
    #dest_mbox.lock()  # lock de mbox file

    if os.path.isdir(infile_name): #als de opgegeven variabele een directory is wordt deze doorgelopen
        if debug:
            print "Detected directory as input, using directory mode"
        count = 0 # count variabele wordt gedeclareerd met een waarde van 0
        for filename in os.listdir(infile_name): #alle files worden doorlopen
            if filename.split('.')[-1] == "eml": #er wordt gekeken welke files op eml eindigen
                try:
                    fi = open(os.path.join(infile_name, filename), 'r') # deze variabel opent de eml files
                except:
                    sys.stderr.write("Error while opening " + filename + "\n") # als er iets fout gaat geeft hij hier aan bij welk bestand dat is
                    dest_mbox.close() # het bestand wordt gesloten bij errors
                    raise
                addFileToMbox(fi, dest_mbox)
                count += 1 # elke iteratie krijgt de count variabele +1
                fi.close() # de files worden gesloten
        if debug:
            print "Processed " + str(count) + " total files." # geeft met behulp van de count variabele aan hoeveel files er zijn behandeld

    if infile_name.split('.')[-1] == "eml": # dit stuk code wordt uitgevoerd wanneer er een enkele file opgegeven wordt
        if debug:
            print "Detected .eml file as input, using single file mode" # er is een file gedetecteerd
        try:
            fi = open(infile_name, 'r') #open het opgegeven bestand als variabele fi
        except:
            sys.stderr.write("Error while opening " + infile_name + "\n") # foutafhandeling
            dest_mbox.close() # bestand wordt gesloten bij errors
            raise
        addFileToMbox(fi, dest_mbox) # file wordt toegevoegd aan opgegeven destination
        fi.close() #sluit variabele fi

    dest_mbox.close()  # close/unlock the mbox file
    return 0


def addFileToMbox(fi, dest_mbox): # met behulp van deze functie worden de gevonden besatnd toegevoegd aan het output.mbox bestand
    try:
        dest_mbox.add(fi) # fi welk voor de gevonden mbox bestanden staat wordt toegevoegd de opgegeven destinatie
    except:
        dest_mbox.close()
        raise


if __name__ == "__main__":
  
    sys.exit(main(sys.argv))
