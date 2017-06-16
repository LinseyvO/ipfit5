from __future__ import print_function
import hashlib
import os



dirt = './MAIL/' # de zoekdirectory wordt opgegeven
logplace = './MAIL/hashes.txt' # hier moet het hashes.txt bestand aangemaakt worden
log = open(logplace, 'w') # het bestand wordt aangemaakt en er kan naartoe geschreven worden


#in deze dubbele for loop wordt er door de opgegeven 'dirt' directory gelooped en worden alle bestanden die eindigen op mbox in de opgegeven variabel geplaatst
for root,dirs, filenames in os.walk(dirt):
    for f in filenames:
        if f.endswith('.mbox'):
            mboxfile = f
            #print (f)

            getmd5 = hashlib.md5(f).hexdigest() # hier wordt de md5 hashwaarde van 'f' berekend
            getsha1= hashlib.sha1(f).hexdigest() # hier wordt de sha1 hashwaarde van 'f' berekend
            print("De MD5 waarde van "+f +" is:" + getmd5, file = log) # hier wordt de print message toegevoegd aan het log bestand
            print("De SHA1 waarde van "+f + " is:" + getsha1, file = log) # hier wordt de print message toegevoegd aan het log bestand
#nadat de data aan het tekstbestand is toegevoegd sluit het bestand
log.close()








