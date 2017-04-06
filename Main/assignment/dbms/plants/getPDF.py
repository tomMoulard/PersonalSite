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

#global stuff
import os
import glob
import sys

URL = [
"http://plants.usda.gov/java/factSheet"
]

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
    """
    res = ""
    return res

def getTreeFactsSheetLink(responce, pos):
    """
    get the tree Facts Sheet Link
    And update pos
    Return hopfully the right string 
    if the returned resultat is empty, there is no link
    """
    res = ""
    return res

def getTreePlantGuideLink(responce, pos):
    """
    get the tree Plant Guide Link
    And update pos
    Return hopfully the right string 
    if the returned resultat is empty, there is no link
    """
    res = ""
    return res

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
        treeName,           pos = getTreeName(responce, pos)
        treeFactsSheetLink, pos = getTreeFactsSheetLink(responce, pos)
        treePlantGuideLink, pos = getTreePlantGuideLink(responce, pos)
        if len(treeFactsSheetLink) == 0 && len(treePlantGuideLink) == 0:
            #both empty
            ID = 0
        elif len(treeFactsSheetLink) == 0 && len(treePlantGuideLink) != 0:
            #treeFactsSheetLink empty
            ID = 2
        elif len(treeFactsSheetLink) != 0 && len(treePlantGuideLink) == 0:
            #treePlantGuideLink empty
            ID = 1
        elif len(treeFactsSheetLink) != 0 && len(treePlantGuideLink) != 0:
            #both links
            ID = 3
        res.append(treeName, [treeFactsSheetLink, treePlantGuideLink], ID)
        pos += 1
    return res

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
    try: 
        urllib.request.urlretrieve(url, nameOfTheFile)
    except:
        print("The file", nameOfTheFile, "(", url, ")", "was not able to be downloaded")

def main():
    print("Getting PDFS")
    print("(All pdfs are stored just after being downloaded to reduce the RAM usage)")
    files = glob.glob(PDFS + "*.pdf")
    try:
        os.mkdir(PDFS)
    except:
        print(sys.exc_info())
    #get the main responce
    responce      = str(opener.open(URL).read())
    #parse the main responce to fill URLS
    urls2Download = getPDFUrls(responce)
    #download pdfs
    for x in urls2Download:
        download(PDFS + x[0], x[1], x[2])