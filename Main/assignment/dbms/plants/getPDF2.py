# -*- coding: utf-8 -*-
"""
Created on Tue Apr 7 13:00:00 2017

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

def prettyPrintForPlan(l):
    """
    This is a pretty print for a Plan list 
    """
    for x in range(len(l)):
        l[x]

class Plan():
    """
    This is the Class fo the Plan object
    """
    def __init__(self,\
            symbol="",\
            synonym_symbol="",\
            scientific_name="",\
            common_name="",\
            doc_fact_sheet="",\
            pdf_fact_sheet="",\
            doc_plant_guide="",\
            pdf_plant_guide="",\
            pdfs=""):
        self.symbol          = symbol
        self.synonym_symbol  = synonym_symbol
        self.scientific_name = scientific_name
        self.common_name     = common_name
        self.doc_fact_sheet  = doc_fact_sheet
        self.pdf_fact_sheet  = pdf_fact_sheet
        self.doc_plant_guide = doc_plant_guide
        self.pdf_plant_guide = pdf_plant_guide
        self.pdfs            = pdfs #prefix of pdf file

    def __str__(self):
        return self.symbol + "-" + self.scientific_name

    def getNameOfFile(self):
        """
        return the full name of the file 
        """
        return self.pdfs + self.symbol + "-" +\
                self.scientific_name + "-" +\
                self.common_name + ".pdf"

    def getName4PDFFact(self):
        """
        return the full name of the Fact sheet 
        """
        return self.pdfs + self.symbol + "-Fact.pdf"

    def getName4PDFGuide(self):
        """
        return the full name of the Guide sheet 
        """
        return self.pdfs + self.symbol + "-Guid.pdf"

    def printMe(self):
        """
        supposed to be called to print this Plan :)
        """
        print(self.common_name,  "(",  self.pdf_fact_sheet,  ",",  self.pdf_plant_guide, ")")
        
def getToken(responce):
    """
    This parse the main page to gather the token to download the good file
    return the full url wuth the token inside :)
    """
    token = ""
    pos = 0
    ll = len(responce)
    while pos < ll and responce[pos:pos+35] != "<a href=\"downloadData?fileName=plnt":
        pos += 1
    pos += 35
    while pos < ll and responce[pos] != ".":
        token += responce[pos]
        pos   += 1
    #print("token:", token)
    return "https://plants.usda.gov/java/downloadData?fileName=plnt"+token+".txt"

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

def parseFile(responce):
    """
    this is supposed to parse the responce to exctract all the Plants
    and download all pdfs poossibles
    return the list of all Plan object found
    """
    data = []
    lines = responce.split("\\n")
    for line in range(1, len(lines) - 3):
        data            = lines[line].split(",")
        symbol          = data[0][1:-1]
        synonym_symbol  = data[1][1:-1]
        scientific_name = data[2][1:-1]
        common_name     = data[3][1:-1]
        doc_fact_sheet  = data[4][1:-1]
        pdf_fact_sheet  = data[5][1:-1]
        doc_plant_guide = data[6][1:-1]
        pdf_plant_guide = data[7][1:-1]
        if pdf_plant_guide == "/factsheet/pdf/":
            pdf_plant_guide = PREFIX + "plantguide/pdf/pg_" + symbol + ".pdf"
        if pdf_fact_sheet == "/factsheet/pdf/":
            pdf_fact_sheet = PREFIX + "plantguide/pdf/fs_" + symbol + ".pdf"
        p = Plan(symbol,\
            synonym_symbol,\
            scientific_name,\
            common_name,\
            doc_fact_sheet,\
            pdf_fact_sheet,\
            doc_plant_guide,\
            pdf_plant_guide,
            PDFS)
        p.printMe()
        data.append(p)
        #download files
        if p.pdf_plant_guide != "":
            download(p.getName4PDFGuide(), PREFIX + p.doc_fact_sheet)
        if p.pdf_fact_sheet != "":
            download(p.getName4PDFFact(), PREFIX + p.doc_fact_sheet)
    return data

def main():
    print("Getting PDFS (V2)")
    print(
        "(All pdfs are stored after being downloaded to reduce the RAM usage)")
    try:
        os.mkdir(PDFS)  
        
    except:
        #There is already a folder here
        pass
    #open the main page to get a valid token to access the main file
    mainResponce = str(opener.open(MAINURL).read())
    URL = getToken(mainResponce)
    print("Got token :", URL)
    #open and get the responce for URL
    responce = str(opener.open(URL).read())
    print("Got main responce, parsing it")
    #parse the responce to fill a Plant array and download them
    data = parseFile(responce)
    prettyPrintForPlan(data)
    print("Got", len(data), "records")
    return data