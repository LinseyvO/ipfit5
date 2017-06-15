from Tkinter import *
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os
import subprocess as sub

#Maak de GUI
root = Tk()
w = Label(root, fg='blue', bg='white', text="Ipfit5")
w.pack()

def quit():
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

def emlnaarmbox():
    os.system('python emltombox.py')

def emailtocsv():
    os.system('python emailtocsv.py')

def writeheader():
    os.system('python writeheader.py')

def insertintodatabase():
    os.system('python insertintodatabase.py')

#Button voor emlnaarmbox
B = Button(root, pady=10, fg='blue', bg='white', text="Stap 1: Eml naar mbox", command=emlnaarmbox)
B.pack()

#Button voor mboxnaarcsv
B2 = Button(root, pady=10, fg='blue', bg='white', text="Stap 2: Mbox naar csv", command=emailtocsv)
B2.pack()

#Button voor schrijvenheader
B3 = Button(root, pady=10, fg='blue', bg='white', text="Stap 3: Schrijven van header", command=writeheader)
B3.pack()

#Button voor database
B4 = Button(root, pady=10,  fg='blue', bg='white', text="Stap 4: Database", command=insertintodatabase)
B4.pack()

#Menu code
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Bestand", menu=subMenu)
subMenu.add_command(label="Open bestand", command=openBestand)

subMenu.add_separator()

subMenu.add_command(label="Exit", command=quit)

root.geometry('{}x{}'.format(500, 300))
root.mainloop()
