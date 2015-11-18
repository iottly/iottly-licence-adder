#!/usr/bin/python
"""

Copyright 2015 Stefano Terna

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
"""

Copyright 2015 Stefano Terna

Licensed under the Apache License, Version 2.0 (the "License");you may not use this file except in compliance with the License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
"""
Credits: Jens Timmerman

http://stackoverflow.com/questions/151677/tool-for-adding-license-headers-to-source-files/9671565#9671565

This script attempts to add a header to each file in the given directory 
The header will be put the line after a Shebang (#!) if present.
If a line starting with a regular expression 'skip' is present as first line or after the shebang it will ignore that file.
If filename is given only files matchign the filename regex will be considered for adding the license to,
by default this is '*'

usage: python addheader.py headerfile directory [filenameregex [dirregex [skip regex]]]

easy example: add header to all files in this directory:
./addheader.py licenseheader.txt . 

harder example header to all python files in a source directory, exept directories named 'includes' and remove previous header:
python addheader.py licenseheader.txt src/ -fre ".*\.py$" -dre "^((?!includes).)*$" -rm licencetoremove.txt

"""

import argparse
import sys
import os
import re

def writeheader(filename,header,removeheader):
    utfstr = chr(0xef)+chr(0xbb)+chr(0xbf)
    shebstr = '#!'
    docktypestr = '<!DOCTYPE'
    fdata = file(filename,"r+").read()

    isUTF = False
    if (fdata.startswith(utfstr)):
        isUTF = True
        fdata = fdata[3:]

    hasShebang = False
    if (fdata.startswith(shebstr)):
        hasShebang = True
        shebcontent = file(filename,"r+").readline()
        if isUTF:
            shebcontent = shebcontent[3:]
        fdata = fdata[len(shebcontent):]

    hasDocktype  = False
    if (fdata.startswith(docktypestr)):
        hasDocktype = True
        docktypecontent = file(filename,"r+").readline()
        if isUTF:
            docktypecontent = docktypecontent[3:]
        fdata = fdata[len(docktypecontent):]
    
    currentdata = fdata

    if removeheader:
        if removeheader in fdata:
            fdata = fdata.replace(removeheader, "")

    if not header in fdata:
        fdata = header + os.linesep + fdata

    if fdata != currentdata:
        print "updating "+filename
        if (hasShebang):
            fdata = shebcontent + fdata
        if (hasDocktype):
            fdata = docktypecontent + fdata
        if (isUTF):
            fdata = utfstr+fdata
        
        file(filename,"w").write(fdata)

        return 1
    else:
        return 0



def addheader(directory,header,removeheader,filenamereg,dirregex):
    """
    recursively adds a header to all files in a dir
    arguments: see module docstring
    """
    countmodified = 0
    listing = os.listdir(directory)
    
    #for each file/dir in this dir
    for i in listing:
        #get the full name, this way subsubdirs with the same name don't get ignored
        fullfn = os.path.join(directory,i) 
        if os.path.isdir(fullfn): #if dir, recursively go in
            if (dirregex.match(fullfn)):
                countmodified += addheader(fullfn, header,removeheader,filenamereg,dirregex)
        else:
            if (filenamereg.match(fullfn)): #if file matches file regex, write the header
                countmodified += writeheader(fullfn, header,removeheader)

    return countmodified

def main(arguments=sys.argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("headerfile", help="full filepath of header file to add")
    parser.add_argument("directory", help="full path of directory to traverse")
    parser.add_argument("-fre","--fileregex", help="regex to filter filenames", default=".*")
    parser.add_argument("-dre","--dirregex", help="regex to filter directories", default=".*")
    parser.add_argument("-rm","--removeheaderfile", help="full filepath to header file to be removed")


    args = parser.parse_args()

    #compile regex    
    fileregex = re.compile(args.fileregex)
    dirregex = re.compile(args.dirregex)

    #read in the headerfile just once
    headerfile = open(args.headerfile)
    header = headerfile.read()
    headerfile.close()

    #read in the removeheaderfile just once
    removeheader = None
    if args.removeheaderfile:
        removeheaderfile = open(args.removeheaderfile)
        removeheader = removeheaderfile.read()
        removeheaderfile.close()

    countmodified = addheader(args.directory,header,removeheader,fileregex,dirregex)

    print "updated %s files." % countmodified


#call the main method
main()
