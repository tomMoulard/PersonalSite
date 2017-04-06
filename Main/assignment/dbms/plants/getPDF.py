# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm

The goal is to get all pdf and informations of the Web Site $URL
and save them to the folder specified in the CONFIG file
"""

#to get the http responce for files and download some 
import urllib.request
opener = urllib.request.FancyURLopener({})

#PDF
#Please install PyPDF before executing the script
import PyPDF2

#to touch a file
#do : Path("<pathOfTheFileToTouch>").touch()
from pathlib import Path

#global stuff
import os
import glob
import sys

URLPREFIX = "http://plants.usda.gov"
URL       = URLPREFIX + "/java/factSheet"

CONFIG   = "./CONFIG"
PDFS = "/tmp/plant_pdfs/"

def gettingCredsForDB():
    """
    Just used to gather configs
    return PDFS
    """
    config   = open(CONFIG, "r")
    configs  = config.readlines()
    PDFS     = configs[12][:len(configs[12]) - 1]
    return PDFS

PDFS = gettingCredsForDB()

def getTreeName(responce, pos):
    """
    get the tree name
    And update pos
    Return hopfully the right string 
    <name> format : <Symbol>_<Scientific Name>_<Common Name>.pdf
    """
    symbol         = ""
    scientificName = ""
    commonName     = ""
    pos += 10
    ll = len(responce)
    #get the symbol
    while pos < ll and responce[pos] != ">":
        pos += 1
    pos += 1
    while pos < ll and responce[pos] != "<":
        symbol += responce[pos]
        pos += 1
    pos += 5
    #get the scientific name
    while pos < ll and responce[pos:pos+5] != "</td>":
        while pos < ll and responce[pos] != "<":
            scientificName += responce[pos]
            pos += 1
        while pos < ll and responce[pos] != ">":
            pos += 1
        pos += 1
    pos += 2
    #get the common name
    while pos < ll and responce[pos:pos+4] != "<td>":
        pos += 1
    pos += 4
    while pos < ll and responce[pos] != "<":
        commonName += responce[pos]
        pos += 1
    res = symbol + "_" + scientificName + "_" + commonName + ".pdf"
    return res, pos + 2

def getTreeFactsSheetLink(responce, pos):
    """
    get the tree Facts Sheet Link
    And update pos
    Return hopfully the right string 
    if the returned resultat is empty, there is no link
    """
    res = URLPREFIX
    ll = len(responce)
    found = False
    while pos < ll and not found:
        if "<td>" == responce[pos:pos+4]:
            pos += 4
            if "&" != responce[pos]:
                #there is a link
                while pos < ll and responce[pos:pos+6] != "</a><a":
                    pos += 1 
                pos += 7
                while pos < ll and responce[pos] != "\"":
                    res += responce[pos]
                    pos += 1
            found = True
        pos += 1
    return res, pos + 2

def getTreePlantGuideLink(responce, pos):
    """
    get the tree Plant Guide Link
    And update pos
    Return hopfully the right string 
    if the returned resultat is empty, there is no link
    """
    res = ""
    ll = len(responce)
    found = False
    while pos < ll and not found:
        if "<td>" == responce[pos:pos+4]:
            pos += 4
            if "&" != responce[pos]:
                #there is a link
                while pos < ll and responce[pos:pos+6] != "</a><a":
                    pos += 1 
                pos += 7
                while pos < ll and responce[pos] != "\"":
                    res += responce[pos]
                    pos += 1
            found = True
        pos += 1
    return res, pos + 2

def getPDFUrls(responce):
    """
    Just get all pdf's urls in the responce 
    RETURN a list of tuples ("<names>", ["<urls>], "<ID>")
    <name> format : <Symbol>_<Scientific Name>_<Common Name>.pdf
    <ID>: 
        - 0 : No link
        - 1 : Only Fact 
        - 2 : Only Guide 
        - 3 : Both Fact & Guide
    """
    res = []
    pos = 0
    ll = len(responce)
    while pos < ll:
        if responce[pos: pos + 5] == "rowon": #a new tree here
            treeName, pos           = getTreeName(responce, pos)
            treeFactsSheetLink, pos = getTreeFactsSheetLink(responce, pos)
            treePlantGuideLink, pos = getTreePlantGuideLink(responce, pos)
            if len(treeFactsSheetLink) == 0 and len(treePlantGuideLink) == 0:
                #both empty
                ID = 0
            elif len(treeFactsSheetLink) == 0 and len(treePlantGuideLink) != 0:
                #treeFactsSheetLink empty
                ID = 2
            elif len(treeFactsSheetLink) != 0 and len(treePlantGuideLink) == 0:
                #treePlantGuideLink empty
                ID = 1
            elif len(treeFactsSheetLink) != 0 and len(treePlantGuideLink) != 0:
                #both links
                ID = 3
            res.append((treeName, [treeFactsSheetLink, treePlantGuideLink], ID))
        pos += 1
    print(res)
    return res

def _download(nameOfTheFile, url):
    """
    This is just to download the file stored in <url>
    and save it in <nameOfTheFile>
    """
    try: 
        urllib.request.urlretrieve(url, nameOfTheFile)
    except:
        print("The file", nameOfTheFile, "(", url, ")",\
                "was not able to be downloaded")

def download(nameOfTheFile, urls, ID):
    """
    This is supposed to download the <nameOfTheFile> for <urls>
    and save it in <nameOfTheFile>
    if ID == 0:
        Creating a file with only the name
    if ID == 1 or ID == 2:
        Simlpy download the pdf
    if ID == 3:
        Download both pdf and appen them
    Return None
    """
    if ID == 0:
        Path(nameOfTheFile).touch()
    elif ID == 1:
        _download(nameOfTheFile, urls[0])
    elif ID == 2:
        _download(nameOfTheFile, urls[1])
    else: # ID == 3
        #downloading both files
        _download(nameOfTheFile + "(Part1)", urls[0])
        _download(nameOfTheFile + "(Part2)", urls[0])
        #mergin them
        merger = PyPDF2.PdfFileMerger()
        merger.append(open(nameOfTheFile + "(Part1)", "rb"))
        merger.append(open(nameOfTheFile + "(Part2)", "rb"))
        merger.write(nameOfTheFile, "wb")
        #erase the two parts
        os.remove(nameOfTheFile + "(Part1)")
        os.remove(nameOfTheFile + "(Part2)")
        merger.close()

def main():
    print("Getting PDFS")
    print(
        "(All pdfs are stored after being downloaded to reduce the RAM usage)")
    files = glob.glob(PDFS + "*.pdf")
    try:
        os.mkdir(PDFS)
    except:
        #There is already a folder here
        pass
    #get the main responce
    responce      = str(opener.open(URL).read())
    #print(responce)
    #parse the main responce to fill URLS
    urls2Download = getPDFUrls(responce)
    #download pdfs
    for x in urls2Download:
        print("downloading: ", x[0]  +"(to: "+ PDFS + x[0] +")")
        download(PDFS + x[0], x[1], x[2])