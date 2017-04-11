# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:00:00 2017

@author: tm
This file is supposed to gather data from pdfs and from the additionnal web site
and then send it via putInDB
"""
#to send data to the DB
#to use: 
import putInDB

#to get the http response for files
import urllib.request
opener = urllib.request.FancyURLopener({})

#PDF
#Please install PyPDF before executing the script
import PyPDF2

#list files 
import glob

#to touch a file
#do : Path("<pathOfTheFileToTouch>").touch()
from pathlib import Path

#REGULAR EXPRESSIONS
import re

PDFS     = ""
MORETOK  = "https://plants.usda.gov/core/profile?symbol="
COLSMETA = [
    ("Symbol", "VARCHAR", "20"),
    ("Scientific_Name", "VARCHAR", "20"),
    ("Common_Name", "VARCHAR", "20"),
    ("fs_Alternative_Name", "VARCHAR", "20"),
    ("fs_Uses", "VARCHAR", "20"),
    ("pg_Alternative_Common_Name", "VARCHAR", "20"),
    ("pg_Uses", "VARCHAR", "20")] # these are the meta data for the cols

# this is the array containing all the data PrimaryKey already added to the db 
DATAS = []

def gettingCredsForPDF():
    """
    Just used to gather configs
    """
    config   = open(CONFIG, "r")
    configs  = config.readlines()
    PDFS     = configs[12][:len(configs[12]) - 1]
    config.close()
    return PDFS

#To get the Credentials
USER, SERVER, PASSWORD, DB, PDFS, TABLE = gettingCredsForDB()


def getMoreDataFromSite(res):
    """
    This function get more data from the MORETOK + Symbol web page
    and add it to the end of res
    no actual return because of lists
    """
    #Open the web page and get the response
    #actual Symbol is res[0][1]
    #parse it to get more data
    #add it to res
    res.append("")

def getDataFromPDF(file, alreadyThere):
    """
    This function parse the pdf file to get data
    return an array of data to be sent
    This return this array
    """
    res = [""] * 7
    #print(res)
    try:
        raw = PyPDF2.PdfFileReader(file)
        rawer = ""
        #concatenate all the pages of the pdf in one string
        for pageNumber in range(raw.pages.lengthFunction()):
            rawer += raw.getPage(pageNumber).extractText() + "\n"
        rawer = re.sub(" +", " ", rawer.replace("\n", ""))
        #let the parsing begin
        pos = 0
        ll = len(rawer)
        while pos < ll and rawer[pos:pos+5] != "Plant":
            pos += 1
        pos += 6 # the next char should be a F or a G:
        if rawer[pos] == "F": # FactSheet
            t = "F"
        else: #Plan Guide
            t = "G"
        #SYMBOL
        #Can be get from the file name : /tmp/plant_pdfs/pg_brca5.pdf
        #AKA <PDFS>/<type>_<symbol>.pdfs
        #But there is some mistakes in the source pdf names
        #-> Need to parse the pdf
        while pos < ll and rawer[pos:pos+9] != "symbol = ":
            pos += 1
        pos += 9 #until the next \\, this should be the symbol
        while pos < ll and rawer[pos] != "\\":
            res[0] += rawer[pos]
            pos += 1
        #SCIENTIFIC NAME & COMMON NAME
        pos = 0
        while pos < ll and rawer[pos:pos+8] != ".gov> \n ":
            pos += 1
        pos += 8
        while pos < ll and rawer[pos] != "\\":
            tmp += rawer[pos]
            pos += 1
        phrase = tmp.split(" ")
        for word in phrase:
            if word[1:].islower(): #COMMON NAME is written in upper cases
                res[1] += word.capitalize() + " " #SCIENTIFIC NAME
            else:
                res[2] += word.capitalize() + " " #COMMON NAME
        if t == "F": #This is a Fact Sheet
            paragraphs = rawer.split('Alternate Names',1)
            if(len(paragraphs) == 1):
                tmpRes = paragraphs[0]
            else:
                tmpRes = paragraphs[1]
            tmpUse = tmpRes.split('Uses', 1)
            if(len(tmpUse) == 1):
                tmpUse = tmpRes.split('Description', 1)
            if(len(paragraphs) > 1):
                res[3] = tmpUse[0]
            paragraphs = tmpUse[1].split('Status', 1)
            if(len(paragraphs) > 1):
                res[4] = paragraphs[0]
            else:
                res[4] = tmpUse[1].split('Description', 1)[0]
        else: # this is a Plan Guide
            paragraphs = re.split('(Alternate common names|Alternate Names)',\
                                    rawer,1)
            if(len(paragraphs) == 1):
                tmpRes = paragraphs[0]
            else:
                tmpRes = paragraphs[2]
            tmpUse = tmpRes.split('Uses', 1)
            if(len(tmpUse) == 1):
                tmpUse = tmpRes.split('Description', 1)
            if(len(paragraphs) > 1):
                res[5] = tmpUse[0]
            paragraphs = tmpUse[1].split('Status', 1)
            if(len(paragraphs) > 1):
                res[6] = paragraphs[0]
            else:
                res[6] = tmpUse[1].split('Description', 1)[0]
    except:
        print("ousp:", file)
        print(sys.exc_info())
        Path(PDFS + "/debug.tmp").touch()
        f = open(PDFS + "/debug.tmp", "r+")
        f.write(file + " has failed because of:" + str(sys.exc_info()))
        f.close()
    return res


def main():
    putInDB.goToDB()
    putInDB.goToTable(tableMeta)
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", file[file])
        d = getDataFromPDF(files[file])
        alreadyThere = d[0][1] in DATAS
        if not alreadyThere:
            DATAS.append(d[0][1])
            d += getMoreDataFromSite(d)
        putInDB.sendDataToDB(d, alreadyThere)