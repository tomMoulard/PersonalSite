# -*- coding: utf-8 -*-
"""
Created on Tue Apr 8 13:00:00 2017

@author: tm

The goal is to get all pdf and informations of the Web Site $URL
and save them to the folder specified in the CONFIG file

VERSION: using this : 
https://plants.usda.gov/java/downloadData?fileName=plnt17240.txt
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

import os
import time

URL     = "https://plants.usda.gov/java/downloadData?fileName=plnt17240.txt"
CONFIG  = "./CONFIG"
PDFS    = "/tmp/plant_pdfs/"
SAVE    = "/tmp/plant_pdfs/data.link"
MAINURL = "https://plants.usda.gov/java/factSheet"
PREFIX  = "https://plants.usda.gov"

def gettingCredsForDB():
    """
    Just used to gather configs
    return PDFS
    """
    config   = open(CONFIG, "r")
    configs  = config.readlines()
    PDFS     = configs[12][:len(configs[12]) - 1]
    SAVE     = configs[15][:len(configs[15]) - 1]
    return PDFS

PDFS = gettingCredsForDB()

def prettyPrintForList(l):
    """
    This is a pretty print fo any list 
    """
    for x in range(len(l)):
        print(x, l[x])
    print("len(list)=", len(l))

def download(nameOfTheFile, url, debug=""):
    """
    This is just to download the file stored in <url>
    and save it in <nameOfTheFile>
    <debug> is optionnal and will be printed before the line
    """
    try: 
        print(debug, "downloading: ", nameOfTheFile  +"(from: "+ url +")")
        urllib.request.urlretrieve(url, nameOfTheFile)
    except:
        print("The file", nameOfTheFile, "(", url, ")",\
                "was not able to be downloaded")

def getName(link):
    """
    This return a proper name for the pdf
    """
    res = PDFS
    partsOfLink = link.split("/")
    return res + partsOfLink[-1]

def main():
    """
    this time simply get all pdf links of the page, download them and store them 
    """
    print("Getting PDFS (V3)")
    print(
        "(All pdfs are stored after being downloaded to reduce the RAM usage)")
    try:
        os.mkdir(PDFS)
    except:
        #There is already a folder here
        pass
    #open the main page to get a valid token to access the main file
    mainResponce = str(opener.open(MAINURL).read())
    print("Got responce, splitting it")
    links = mainResponce.split(".pdf")
    print("Responce splited, Downloading pdfs")
    pdfs = []
    pos = 0
    for pdf in links:
        tmp = ""
        tmpLinks = pdf.split("\"")
        tmp = PREFIX + tmpLinks[-1] + ".pdf"
        pdfs.append(tmp)
        download(getName(tmp), tmp, debug=pos)
        pos += 1
        time.sleep(1)