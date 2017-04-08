# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm
The goal is to lookup all pdfs and store the information they contain in
The DataBase with the credentials stored on the CONFIG file
V2
"""

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
TABLE    = "plant"

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
    if(DB == "None"):
        DB = str(t[0]) + "-"\
            + str(t[1]) + "-"\
            + str(t[2]) + "_"\
            + str(t[3]) + ":"\
            + str(t[4]) + ":"\
            + str(t[5]) + "_"\
            + "plants"
    TABLE = str(t[0]) + "-"\
        + str(t[1]) + "-"\
        + str(t[2]) + "_"\
        + str(t[3]) + ":"\
        + str(t[4]) + ":"\
        + str(t[5]) + "_"\
        + "plants"
    return USER, SERVER, PASSWORD, DB, PDFS, TABLE

#To get the Credentials
USER, SERVER, PASSWORD, DB, PDFS, TABLE = gettingCredsForDB()
db = MySQLdb.connect(SERVER, USER, PASSWORD)
CURSOR = db.cursor()

def exe(code):
    """
    This is only used to send a "code" to mysql
    """
    print(USER + "@" + SERVER + "> " + code)
    try:
        CURSOR.execute(code)
    except:
        print(sys.exc_info())

def getDataFromPDF(file):
    """
    This function parse the pdf file to get data
    return an array of data to be sent:
        The list resulting should contain:
         0 : Symbol
         1 : Scientific Name
         2 : Common Name
         3 : fs_Alternative_Name
         4 : fs_Uses
         5 : pg_Alternative_Common_Name
         6 : pg_Uses
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
        #print([rawer.split("\n")])
        #let the parsing begin
    except:
        print("ousp:", file)
        print(sys.exc_info())
        Path(PDFS + "/debug.tmp").touch()
        f = open(PDFS + "/debug.tmp", "r+")
        f.write(file + " has failed")
        f.close()
    return res

def sendDataToDB(data, ):
    """
    This is used so select which data and who to send the to the db
    the table should be ready to accept data
    """
    exe("SHOW databases;")

def main():
    print("Connected to server", SERVER, "with credential for :", USER)

    TABLE = """
        DROP TABLE IF EXISTS plants;
        CREATE TABLE plants (
            Symbol                      VARCHAR(10) PRIMARY KEY NOT NULL,
            Scientific_Name             VARCHAR(60) NOT NULL,
            Common_Name                 VARCHAR(42) NOT NULL,
            fs_Alternative_Name         VARCHAR(4096),
            fs_Uses                     VARCHAR(4096),
            pg_Alternative_Common_Name  VARCHAR(4096),
            pg_Uses                     VARCHAR(4096)
        ) ENGINE=InnoDB;
    """
    exe(TABLE)
    print("Table", DB, "Created")
    print("Opening pdfs parse them and store data in the db")
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", file[file])
        d = getDataFromPDF(files[file])
        sendDataToDB(d)
    print("closing DB")
    db.close()