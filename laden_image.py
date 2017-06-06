import sys
import pytsk3
import datetime
import pyewf
import argparse
import os
import re


class ewf_Img_Info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()


def directoryRecurse(directoryObject, parentPath):
    for entryObject in directoryObject:
        if entryObject.info.name.name in [".", ".."]:
            continue

        try:
            f_type = entryObject.info.meta.type
        except:
            print "Cannot retrieve type of", entryObject.info.name.name
            continue

        try:

            filepath = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name)
            outputPath = './%s/%s/' % (str(partition.addr), '/'.join(parentPath))

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entryObject.as_directory()
                parentPath.append(entryObject.info.name.name)
                directoryRecurse(sub_directory, parentPath)
                parentPath.pop(-1)
                print "Directory: %s" % filepath

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:
                searchResult = re.match(args.search, entryObject.info.name.name)
                if not searchResult:
                    continue
                filedata = entryObject.read_random(0, entryObject.info.meta.size)
                if args.extract == True:
                    if not os.path.exists(outputPath):
                        os.makedirs(outputPath)
                    extractFile = open(outputPath + entryObject.info.name.name, 'w')
                    extractFile.write(filedata)
                    extractFile.close

        except IOError as e:
            print e
            continue

argparser = argparse.ArgumentParser(
    description='Extract the $MFT from all of the NTFS partitions of an E01')
argparser.add_argument(
    '-i', '--image',
    dest='imagefile',
    action="store",
    type=str,
    default=None,
    required=True,
    help='E01 to extract from'
)

argparser.add_argument(
  '-s', '--search',
  dest='search',
  action="store",
  type=str,
  default='*',
  required=False,
  help='Specify search parameter e.g. *.Ink'
)

argparser.add_argument(
  '-e', '--extract',
  dest='extract',
  action="store_true",
  default=False,
  required=False,
  help='Pass this option to extract files found'
)

argparser.add_argument(
  '-t', '--type',
  dest='imagetype',
  type=str,
  default=False,
  required=True,
  help='Specify image type e01 or raw'
)
args = argparser.parse_args()
dirPath = '/'

if not args.search == '.*':
    print "Search Term Provided", args.search


if (args.imagetype == "e01"):
    filenames = pyewf.glob(args.imagefile)
    ewf_handle = pyewf.handle()
    ewf_handle.open(filenames)
    imagehandle = ewf_Img_Info(ewf_handle)

elif (args.imagetype == "raw"):
    print "Raw Type"
    imagehandle = pytsk3.Img_Info(url=args.imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)

for partition in partitionTable:
    print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
    try:
        filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512))
    except:
        print "Partition has no supported file system"
        continue

    print "File System Type Dectected ",filesystemObject.info.ftype
    directoryObject = filesystemObject.open_dir(path=dirPath)
    print "Directory:", dirPath
    directoryRecurse(directoryObject, [])