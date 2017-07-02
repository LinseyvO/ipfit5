import sys
import pytsk3
import datetime
import pyewf
import argparse
import os
import re


class ewf_Img_Info(pytsk3.Img_Info): # er wordt een class aangemaakt gebaseerd op pytsk's img info die pyewf supported formats kan behandleen
    def __init__(self, ewf_handle): # constructor met parameters zichzelf en een ewf_handle object
        self._ewf_handle = ewf_handle # een referentie naar de ewf_handle wordt in de class opgeslagen als ewf_handle
        super(ewf_Img_Info, self).__init__( # hiermee wordt de constructor opgeroepen van de class die geerfd wordt.
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL) # wanneer de parent constructor wordt geroepen moeten er twee variabelen meegegeven worden. de url en het type

    def close(self): 
        self._ewf_handle.close() # deze roept de ewf_handle object close aan inplaats van de img_info close methode

    def read(self, offset, size): # deze functie neemt de offset van waar hij moet beginnen met readen en de totale size die gelezen moet worden
        self._ewf_handle.seek(offset) # lees de offset
        return self._ewf_handle.read(size) # return de grootte

    def get_size(self): # deze functie returned de totale size van de media inplaats van de standaard img_info get_size methode
        return self._ewf_handle.get_media_size()


def directoryRecurse(directoryObject, parentPath): # functie met parameters
    for entryObject in directoryObject: # loop door directory entries in een directory
        if entryObject.info.name.name in [".", ".."]: # kijk naar huidige directory en parent directory
            continue

        try:
            f_type = entryObject.info.meta.type # als deze variabele assigned wordt gaat de code verder
        except:
            print "Cannot retrieve type of", entryObject.info.name.name # error afhandeling
            continue

        try:

            filepath = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name) # hier wordt het huidige volle pad opgeslagen
            outputPath = './%s/%s/' % (str(partition.addr), '/'.join(parentPath)) # vang het volledige pad van de file die waarnaar wordt gezocht

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR: #kijk of de f_type variabele gelijk is aan de waarde die staat voor een directory
                sub_directory = entryObject.as_directory() # stop een directory object in een variabel
                parentPath.append(entryObject.info.name.name) # voeg de naam van de directory die wordt bekeken toe aan deze variabele
                directoryRecurse(sub_directory, parentPath) # de functie wordt aangeroepen maar nu in een sub directory
                parentPath.pop(-1) # verwijder het laatste element uit de lijst
                print "Directory: %s" % filepath # print het bekeken paden

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0: # afhandeling van non zero sized files die geinspecteerd worden
                searchResult = re.match(args.search, entryObject.info.name.name) # hier wordt gezocht naar het bestand en als er iets wordt gevonden het wordt het object gereturned en opgeslagen in de searchResult variabele
                if not searchResult: # test om te kijken dat wanneer er geen matches zijn de searchResult variabele leeg is
                    continue
                filedata = entryObject.read_random(0, entryObject.info.meta.size)
                if args.extract == True: # kijken of er een extract is meegegeven
                    if not os.path.exists('./mail/'): # kijk of de opgegeven directory bestaat
                        os.makedirs('./mail/') # maak de directory aan als deze niet bestond
                    extractFile = open('./mail/' + entryObject.info.name.name, 'w') # extract naar het opgegeven pad
                    extractFile.write(filedata) # schrijf de data
                    extractFile.close # close de handle aangezien deze nog gebruikt moet worden

        except IOError as e:
            print e
            continue

argparser = argparse.ArgumentParser( # commandline parameters worden hier toegevoegd
    description='Extract the $MFT from all of the NTFS partitions of an E01')
argparser.add_argument(
    '-i', '--image', # dit moet de gebruiker invoeren om dit argument te gebruiken
    dest='imagefile', # in deze variabele wordt het parsed argument opgeslagen
    action="store", # geef aan dat het moet worden opgeslagen
    type=str, # sla het op als een string
    default=None, # er is geen default image name
    required=True, # geeft aan dat deze parameter moet worden meegegeven om het programmma te runnen
    help='E01 to extract from'
)

argparser.add_argument( # commandline parameters worden hier toegevoegd
  '-s', '--search', # dit moet de gebruiker invoeren om dit argument te gebruiken
  dest='search', # in deze variabele wordt het parsed argument opgeslagen
  action="store", # geef aan dat het moet worden opgeslagen
  type=str, # sla het op als een string
  default=False,
  required=False, # geeft aan dat deze parameter niet moet worden meegegeven om het programmma te runnen
  help='Specify search parameter e.g. *.Ink'
)

argparser.add_argument( #commandline parameters worden hier toegevoegd
  '-e', '--extract', # dit moet de gebruiker invoeren om dit argument te gebruiken
  dest='extract', # in deze variabele wordt het parsed argument opgeslagen
  action="store_true", # als er met -e iets owrdt meegegeven is het True anders is het False
  default=True,
  required=False, # geeft aan dat deze parameter niet moet worden meegegeven om het programmma te runnen
  help='Pass this option to extract files found'
)

argparser.add_argument( # commandline parameters worden hier toegevoegd
  '-t', '--type', # dit moet de gebruiker invoeren om dit argument te gebruiken
  dest='imagetype', # in deze variabele wordt het parsed argument opgeslagen
  type=str, # sla het op als een string
  default=False,
  required=True, # geeft aan dat deze parameter moet worden meegegeven om het programmma te runnen
  help='Specify image type e01 or raw'
)
args = argparser.parse_args() # de argumenten worden nu geparsed
dirPath = '/'

if not args.search == '.*':
    print "Search Term Provided", args.search # geeft de zoekterm terug en geeft aan dat er iets gebeurt


if (args.imagetype == "e01"): # voer dit uit wanneer het e01 type wordt gegeven
    filenames = pyewf.glob(args.imagefile) # de image uit de -i parameter wordt gepakt
    ewf_handle = pyewf.handle()
    ewf_handle.open(filenames)
    imagehandle = ewf_Img_Info(ewf_handle)

elif (args.imagetype == "raw"): # voer dit uit wanneer het e01 type wordt gegeven
    print "Raw Type"
    imagehandle = pytsk3.Img_Info(url=args.imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)

for partition in partitionTable:
    print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len # er gaat gekeken worden of het partitie type supported is
    try:
        filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512)) # er wordt van alle partities gekeken of deze geopend kan worden
    except:
        print "Partition has no supported file system" # wanneer een partitie niet geopend kan worden
        continue

    print "File System Type Detected ", filesystemObject.info.ftype # als de partitie gesupport is werkt de code zonder problemen
    directoryObject = filesystemObject.open_dir(path=dirPath) # een object wordt aangemaakt met een lijst van alle files en directories in een directory
    print "Directory:", dirPath
    directoryRecurse(directoryObject, [])
