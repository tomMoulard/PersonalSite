# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm
The goal is to lookup all pdfs and store the information they contain in
The DataBase with the credentials stored on the CONFIG file
V2
"""

#to get the http response for files
import urllib.request
opener = urllib.request.FancyURLopener({})

#Usefull stuff
import random
import time
import sys

#mysql
#Please install python-mysqldb 
#or python3-mysqldb before executing the script
import MySQLdb

#PDF
#Please install PyPDF before executing the script
import PyPDF2

#password
import getpass

#list files 
import glob

#to touch a file
#do : Path("<pathOfTheFileToTouch>").touch()
from pathlib import Path

#REGULAR EXPRESSIONS
import re

#credentials
#mysql -u 16920041 -h 172.31.34.145 -p
SN       = "16920041"
USER     = SN
SERVER   = "172.31.34.145"
PASSWORD = SN
DB       = "db" + SN
CURSOR   = None;
CONFIG   = "./CONFIG"
PDFS     = "/tmp/plant_pdfs" 
TABLE    = "usdaplant"
MORETOK  = "https://plants.usda.gov/core/profile?symbol="
COLS     = ["fs_Alternative_Name",\
            "fs_Uses",\
            "pg_Alternative_Common_Name",\
            "pg_Uses"] # these are TABLE's COLS name
TYPECOLS = ["VARCHAR"] * len(COLS) # theses are CLOs TYPE
LENCOLS  = ["10"]      * len(COLS) # theses are COLs lenght

def prettyPrintForList(l):
    """
    This is a pretty print fo any list 
    """
    for x in range(len(l)):
        print(x, l[x])

def gettingCredsForDB():
    """
    Just used to gather configs
    return USER, SERVER, PASSWORD, DB, PDFS
    """
    print("Getting credentials")
    config   = open(CONFIG, "r")
    configs  = config.readlines()
    #prettyPrintForList(configs)
    USER     = configs[0][:len(configs[0]) - 1]
    SERVER   = configs[3][:len(configs[3]) - 1]
    PASSWORD = configs[6][:len(configs[6]) - 1]
    DB       = configs[9][:len(configs[9]) - 1]
    PDFS     = configs[12][:len(configs[12]) - 1]
    if(PASSWORD == "None"):
        PASSWORD = getpass.getpass()
    t = time.localtime()
    #USE DATABASE
    #if NO database create one :)
    if(DB == "None"):
        DB = str(t[0])  + "_"\
            + str(t[1]) + "_"\
            + str(t[2]) + "_"\
            + str(t[3]) + "h"\
            + str(t[4]) + "m"\
            + str(t[5]) + "s_"\
            + "plants"
    TABLE = str(t[0]) + "_"\
        + str(t[1]) + "_"\
        + str(t[2]) + "_"\
        + str(t[3]) + "h"\
        + str(t[4]) + "m"\
        + str(t[5]) + "s_"\
        + "plants"
    return USER, SERVER, PASSWORD, DB, PDFS, TABLE

#To get the Credentials
USER, SERVER, PASSWORD, DB, PDFS, TABLE = gettingCredsForDB()
db = MySQLdb.connect(SERVER, USER, PASSWORD)
CURSOR = db.cursor()

def exe(code, optionnalOutput=""):
    """
    This is only used to send a "code" to mysql
    and print optionnalOutput after this :)
    """
    print(USER + "@" + SERVER + "> " + code, optionnalOutput)
    try:
        CURSOR.execute(code)
    except:
        print(sys.exc_info())

def getMoreData(res):
    """
    This function get more data from the MORETOK + Symbol web page
    and add it to the end of res
    no actual return because of lists
    """
    #Open the web page and get the response
    #actual Symbol is res[0]
    #parse it to get more data
    #add it to res
    res.append("")

def getDataFromPDF(file):
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
        getMoreData(res)
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

def changeColSize(colPos, newSize):
    """
    This function change the colName size
    """
    val = "ALTER TABLE " + TABLE + " MODIFY " + colPos + " " +\
        TYPECOLS[colPos] + "(" + newSize + ");"
    LENCOLS[colPos] = max(newSize, LENCOLS[colPos])
    exe(val)

def sendDataToDB(data):
    """
    This is used so select which data and who to send the to the db
    the table should be ready to accept data
    INSERT + 
    """
    INS = "INSERT INTO " + TABLE + " (Symbol, Scientific_Name, Common_Name"
    for col in COLS:
        INS += ", " + col
    INS += ")"
    VAL = "VALUES (" + data[0] + ", " + data[1] + ", " + data[2]
    for index in range(len(COLS)):
        VAL += ", " + data[index]
    VAL+= ");"
    try:
        exe(INS + VAL)
    except:
        #The line is already there
        if data[3] != "": #AKA data come from a Fact sheet
            if len(data[3]) > LENCOLS[3]:
                changeColSize(3, len(data[3]))
            if len(data[4]) > LENCOLS[4]:
                changeColSize(4, len(data[4]))
            val = "UPDATE " + TABLE + " WHERE Symbol = " + data[0] +\
                " SET fs_Alternative_Name = " + data[3] + ", "\
                "fs_Uses = " + data[4]
            for x in rang(7, len(data)):
                #if not data[x] in COLS: # data is not in the cols
                #    addCol(data[x][:6], size=str(len(data[x])))
                if len(data[x]) > LENCOLS[x]:
                    changeColSize(x, len(data[x]))
                var += ", " + COLS[x] + " = " + data[x]
            exe(var + ";")
        else:#AKA data come from a Plan Guide
            var = "UPDATE " + TABLE + " WHERE Symbol = " + data[0]
            for x in rang(5, len(data)):
                #if not data[x] in COLS: # data is not in the cols
                #    addCol(data[x][:6], size=str(len(data[x])))
                if len(data[x]) > LENCOLS[x]:
                    changeColSize(x, len(data[x]))
                var += ", " + COLS[x] + " = " + data[x]
            exe(var + ";")
        
def addCol(colName, typeCols="VARCHAR", size="64"):
    """
    This symply add a new colone to the TABLE
    Called colName
    and update COLS
    """
    COLS.append(colName)
    LENCOLS.append(size)
    TYPECOLS.append(typeCols)
    exe("ALTER TABLE "+TABLE+" ADD COLUMN "+colName+" "+typeCols+"("+size+");")

def main():
    print("Connected to server", SERVER, "with credential for :", USER)
    try :
        exe("CREATE DATABASE IF NOT EXISTS " + DB + ";")
    except:
        print("Database is existent")
    try:
        exe("USE " + DB +";")
    except:
        print("already using database ?")
    CREATETABLE = """
        DROP TABLE IF EXISTS """ + TABLE + """;
        CREATE TABLE """ + TABLE + """(
            Symbol          VARCHAR(10) PRIMARY KEY NOT NULL,
            Scientific_Name VARCHAR(60) NOT NULL,
            Common_Name     VARCHAR(42) NOT NULL"""
    for x in rang(len(data)):
        var += ", " + COLS[x] + " = " + data[x]
    CREATETABLE += ") ENGINE=InnoDB"
    exe(CREATETABLE)
    print("Table", TABLE, "Created")
    print("Opening pdfs parse them and store data in the db")
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", file[file])
        d = getDataFromPDF(files[file])
        sendDataToDB(d)
    print("closing DB")
    db.close()