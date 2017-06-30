from Tkinter import *
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os
import subprocess as sub

#Maak de GUI
root = Tk()
w = Label(root, fg='white', bg='black', text="Ipfit5 Opdracht C Groep 8")
w.pack()

def quit(): #deze functie zorgt ervoor dat de GUI afgesloten kan worden.
    root.destroy()

def openBestand():
    root.filename = tkFileDialog.askopenfilename(filetypes=(("E01 File", "*.E0*"), ("AFF", "*.aff"), ("RAW", ".raw"), ("All files", "*.*")))
    f = open(root.filename)
    print(root.filename) #geeft pad naar bestand

    # Het imagebestand opgeven
    output = "python laden_image.py -i "
    image = tkSimpleDialog.askstring("Kies het imagetype", "'e01', 'raw'")
    print output

    # Zoekfunctie opgeven
    zoekterm = tkSimpleDialog.askstring("Geef de zoekterm op", "'.*\.pst', '.*\.mbox', '.*\.eml'")
    print output

    # verwerken van opgegeven data
    output += root.filename
    output += " -t " + image + " -s " + zoekterm
    print output
    os.system(output)

'''
Hieronder zijn de functies weergegeven die de knoppen gebruiken in de GUI.
Deze functies bevatten allemaal terminal commands en deze worden zo uitgevoerd.
'''
def emlnaarmbox():
    os.system('python emltombox.py')

def emailtocsv():
    os.system('python emailtocsv.py')

def writeheader():
    os.system('python writeheader.py')

def insertintodatabase():
    os.system('python insertintodatabase.py')

def hashenmd5():
    os.system('md5sum ./mail/* >> ./mail/md5hashes.txt')

def hashensha1():
    os.system('sha1sum ./mail/* >> ./mail/sha1hashes.txt')

def query():
    os.system('cp ./mail/clean_mail.csv ./mail/overzicht.csv')

'''
Hieronder zijn alle knoppen met daarbij de functies waarnaar ze verwijzen weergegeven.
Pady en padx zorgen ervoor dat de knoppen even groot en even lang zijn.
fg en bg geven de tekst en de achtergrond een kleur, bij alle knoppen is dit witte tekst en zwarte achtergrond.
text is de tekst van de knippen.
command bevat de functie waar de knop gebruik van maakt.
'''

#Button voor emlnaarmbox
B = Button(root, pady=10, padx=37, fg='white', bg='black', text="Stap 1: Eml naar mbox", command=emlnaarmbox)
B.pack()

#Button voor mboxnaarcsv
B2 = Button(root, pady=10, padx=39, fg='white', bg='black', text="Stap 2: Mbox naar csv", command=emailtocsv)
B2.pack()

#Button voor schrijvenheader
B3 = Button(root, pady=10, padx=19, fg='white', bg='black', text="Stap 3: Schrijven van header", command=writeheader)
B3.pack()

#Button voor database
B4 = Button(root, pady=10, padx=55, fg='white', bg='black', text="Stap 4: Database", command=insertintodatabase)
B4.pack()

#Button voor hashen md5
B5 = Button(root, pady=10, padx=23, fg='white', bg='black', text="MD5-hashen van bestanden", command=hashenmd5)
B5.pack()

#Button voor hashen sha1
B7 = Button(root, pady=10, padx=20, fg='white', bg='black', text="SHA1-hashen van bestanden", command=hashensha1)
B7.pack()

#Button voor query
B6 = Button(root, pady=10, padx=50,  fg='white', bg='black', text="Genereer overzicht", command=query)
B6.pack()

#Menu code
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Bestand", menu=subMenu)
subMenu.add_command(label="Open bestand", command=openBestand)

subMenu.add_separator()

subMenu.add_command(label="Exit", command=quit)

root.geometry('{}x{}'.format(500, 300)) #dit zorgt ervoor dat het scherm een vaste grote heeft bij het opstarten
root.mainloop()