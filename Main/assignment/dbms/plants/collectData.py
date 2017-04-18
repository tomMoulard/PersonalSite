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

#Parsing lib
import bs4 as bs

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

#used to generate false data
import random

#to get better error messages
import sys



PDFS     = ""
CONFIG   = "./CONFIG"
MORETOK  = "https://plants.usda.gov/core/profile?symbol="
COLSMETA = [
    ("Symbol", "VARCHAR", "20"),
    ("Scientific_Name", "VARCHAR", "20"),
    ("Common_Name", "VARCHAR", "20"),
    ("fs_Alternative_Name", "VARCHAR", "200"),
    ("fs_Uses", "VARCHAR", "200"),
    ("pg_Alternative_Common_Name", "VARCHAR", "200"),
    ("pg_Uses", "VARCHAR", "200")] # these are the meta data for the cols

FAKEDATA = [
    ("Symbol", "TEST"),
    ("Scientific_Name", "THIS IS A TEST"),
    ("Common_Name", "TESTTEST"),
    ("fs_Alternative_Name", "Why not test it"),
    ("fs_Uses", "TESTING"),
    ("pg_Alternative_Common_Name", "TEST SOUNDS GOOD"),
    ("pg_Uses", " test"),
    ("test_test", "Well if this works .. <3")
]


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
PDFS = gettingCredsForPDF()

def generateString(l):
    """
    Just give a number and
    return a random string 
    """
    res = ""
    for x in range(l):
        res += chr(random.randint(97, 122)) 
    return res

def generateFakeData():
    """
    This is just for testing purpose
    generate a false data set, quite messy to use :/
    """
    res =  [
    ("Symbol", generateString(random.randint(1, 15))),
    ("Scientific_Name", generateString(random.randint(5, 20))),
    ("Common_Name", generateString(random.randint(10, 25))),
    ("fs_Alternative_Name", generateString(random.randint(0, 122))),
    ("fs_Uses", generateString(random.randint(50, 200))),
    ("pg_Alternative_Common_Name", generateString(random.randint(25, 250))),
    ("pg_Uses", generateString(random.randint(10, 30)))]
    nb = random.randint(1, 10)
    for x in range(nb):
        res.append((str(x) + generateString(5), generateString(random.randint(1, 20))))
    return res

def getMoreDataFromSite(res):
    """
    This function get more data from the MORETOK + Symbol web page
    and add it to the end of res
    no actual return because of lists
    """
    #Open the web page and get the response
    #actual Symbol is res[0][1]
    #parse it to get more data
    #add it to resres = []
    mainresponse = str(opener.open(MORETOK + res[0][1]).read())
    if "No Data Found" in mainresponse:
        print("No Data Found for: ", res[0][1])
    else:
        soup = bs.BeautifulSoup(mainresponse, "lxml")

def getDataFromPDF(file):
    """
    This function parse the pdf file to get data
    return an array of data to be sent
    This return this array
    """
    res = []
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
        name = ""
        fileContent = rawer.split("Symbol = ",1)
        pos = 0
        ll = len(fileContent[1])
        while pos < ll and fileContent[1][pos] != " ":
            name += fileContent[1][pos]
            pos += 1
        res.append(("Symbol", name))
        #SCIENTIFIC NAME & COMMON NAME
        pos = 0
        while pos < ll and rawer[pos:pos+8] != ".gov> \n ":
            pos += 1
        pos += 8
        tmp = ""
        while pos < ll and rawer[pos] != "\\":
            tmp += rawer[pos]
            pos += 1
        phrase = tmp.split(" ")
        tmp1, tmp2 = "", ""
        for word in phrase:
            if word[1:].islower(): #COMMON NAME is written in upper cases
                tmp1 += word.capitalize() + " " #SCIENTIFIC NAME
            else:
                tmp2 += word.capitalize() + " " #COMMON NAME
        res.append(("Scientific_Name", tmp1))
        res.append(("Common_Name", tmp2))
        if t == "F": #This is a Fact Sheet
            #thanks Mathis <3
            paragraphs = rawer.split("Alternate Names",1)
            if(len(paragraphs) == 1):
                tmpRes = paragraphs[0]
            else:
                tmpRes = paragraphs[1]
            tmpUse = tmpRes.split("Uses", 1)
            if(len(tmpUse) == 1):
                tmpUse = tmpRes.split("Description", 1)
            res.append(("fs_Alternative_Name", tmpUse[0]))
            paragraphs = tmpUse[1].split("Status", 1)
            if(len(paragraphs) > 1):
                res.append(("fs_Uses", paragraphs[0]))
            else:
                res.append(("fs_Uses", tmpUse[1].split("Description", 1)[0]))
        else: # this is a Plan Guide
            paragraphs = re.split("(Alternate common names|Alternate Names)",\
                                    rawer,1)
            if(len(paragraphs) == 1):
                tmpRes = paragraphs[0]
            else:
                tmpRes = paragraphs[2]
            tmpUse = tmpRes.split("Uses", 1)
            if(len(tmpUse) == 1):
                tmpUse = tmpRes.split("Description", 1)
            res.append(("pg_Alternative_Common_Name", tmpUse[0]))
            paragraphs = tmpUse[1].split("Status", 1)
            if(len(paragraphs) > 1):
                res.append(("pg_Uses", paragraphs[0]))
            else:
                res.append(("pg_Uses", tmpUse[1].split("Description", 1)[0]))
    except:
        print("ousp:", file)
        print(sys.exc_info())
        Path(PDFS + "/debug.tmp").touch()
        f = open(PDFS + "/debug.tmp", "r+")
        last = f.read()
        f.write(last + "\n" + file + " has failed because of:" + str(sys.exc_info()) + "\n"\
            + "Data: " + str(res)
            )
        f.close()
    return res


def main():
    putInDB.goToDB()
    putInDB.goToTable(COLSMETA)
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", files[file])
        d = getDataFromPDF(files[file])
        #if not putInDB.isAlreadyThere(d[0][1])
        #    d += getMoreDataFromSite(d)
        if d:
            putInDB.sendDataToDB(d, COLSMETA)
    putInDB.printTable(COLSMETA)
    putInDB.closeDB()