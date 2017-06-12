from Tkinter import *
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os
#import laden_image

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

#Maak de GUI
root = Tk()
w = Label(root, text="Ipfit5")
w.pack()

#Menu code
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="Bestand", menu=subMenu)
#subMenu.add_command(label="Inladen", command=laden_image)
subMenu.add_command(label="Open bestand", command=openBestand)

subMenu.add_separator()

subMenu.add_command(label="Exit", command=quit)

#Status bar
#status = Label(root, text="Bezig...", bd=1, relief=SUNKEN, anchor=W)
#status.pack(side=BOTTOM, fill=X)

root.geometry('{}x{}'.format(500, 300))
root.mainloop()