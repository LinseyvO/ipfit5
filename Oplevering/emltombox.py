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

    if os.path.isdir(infile_name):
        if debug:
            print "Detected directory as input, using directory mode"
        count = 0
        for filename in os.listdir(infile_name):
            if filename.split('.')[-1] == "eml":
                try:
                    fi = open(os.path.join(infile_name, filename), 'r')
                except:
                    sys.stderr.write("Error while opening " + filename + "\n")
                    dest_mbox.close()
                    raise
                addFileToMbox(fi, dest_mbox)
                count += 1
                fi.close()
        if debug:
            print "Processed " + str(count) + " total files."

    if infile_name.split('.')[-1] == "eml":
        if debug:
            print "Detected .eml file as input, using single file mode"
        try:
            fi = open(infile_name, 'r')
        except:
            sys.stderr.write("Error while opening " + infile_name + "\n")
            dest_mbox.close()
            raise
        addFileToMbox(fi, dest_mbox)
        fi.close()

    dest_mbox.close()  # close/unlock the mbox file
    return 0


def addFileToMbox(fi, dest_mbox):
    # Any additional preprocessing logic goes here, e.g. duplicate filter
    try:
        dest_mbox.add(fi)
    except:
        dest_mbox.close()
        raise


if __name__ == "__main__":
    #if len(sys.argv) != 3:
        #sys.stderr.write("Usage: ./emlToMbox.py input outbox.mbox\n")
        #sys.exit(1)
    sys.exit(main(sys.argv))
