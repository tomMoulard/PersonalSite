# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm
The goal is to lookup all pdfs and store the information they contain in
The DataBase with the credentials stored on the CONFIG file
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

#to get the http responce for files
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
    if(DB == "None"):
        t = time.localtime()
        DB = str(t[0]) + "-"\
            + str(t[1]) + "-"\
            + str(t[2]) + "_"\
            + str(t[3]) + ":"\
            + str(t[4]) + ":"\
            + str(t[5]) + "_"\
            + "plants"
    return USER, SERVER, PASSWORD, DB, PDFS

def exe(code):
    """
    This is only used to send a "code" to mysql
    """
    print(USER + "@" + SERVER + "> " + code)
    try:
        CURSOR.execute(code)
    except:
        print(sys.exc_info())

#To get the Credentials
USER, SERVER, PASSWORD, DB, PDFS = gettingCredsForDB()
db = MySQLdb.connect(SERVER, USER, PASSWORD)
CURSOR = db.cursor()

def getDataFromPDF(file, data=None):
    """
    This function parse the pdf file to get data
    return an array of data to be sent:
        The list resulting should contain:
         0 : Symbol
         1 : Scientific Name
         2 : Common Name
         3 : Synonym Symbol
         4 : 
         5 : 
         6 : fs_Alternative_Name
         7 : fs_Uses
         8 : pg_Alternative_Common_Name
         9 : pg_Uses
         10: pg_Uses
    This return this array
    (To simplifies a little if you gathered the Plan data from getPDF
    you need to give the right Plan object <data> to take less computation)
    """
    res = [""] * 11
    #print(res)
    try:
        raw = PyPDF2.PdfFileReader(file)
        rawer = ""
        #concatenate all the pages of the pdf in one string
        for pageNumber in range(raw.pages.lengthFunction()):
            rawer += raw.getPage(pageNumber).extractText() + "\n"
        #print([rawer.split("\n")])
        #let the parsing begin
        if data == None:
            #Symbol 
            tmp = file.split("\\")
            tmp2 = tmp[-1]
            for x in tmp2:
                if x == "-":
                    break
                else:
                    res[0] += x

            #Scientific name
            pos = 0
            ll = len(rawer)
            while pos < ll:

                pos += 1
        else: # there is data
            res[0] = data.symbol
            res[1] = data.scientific_name
            res[2] = data.common_name
            res[3] = data.synonym_symbol
        #ether way we need to get the data from the file
        #but it splits again between the Fact Sheet and the Plan Guide
        if file[-8:-4] == "Fact": # then this is a FS
            pass
        else: # this is a PG
            pass

    except:
        print("ousp:", file)
        print(sys.exc_info())
    return res

def sendDataToDB(data):
    """
    This is used so select which data and who to send the to the db
    the table should be ready to accept data
    """
    exe("SHOW databases;")

def main(data=None):
    print("Connected to server", SERVER, "with credential for :", USER)
    print("Opening pdfs parse them and store datas in the db")
    #files = glob.glob(PDFS + "*.pdf")
    #for file in range(len(files)):
    #    print("geting data from", file[file])
    #    d = getDataFromPDF(files[file], data=data[file])
    #    sendDataToDB(d)
    d = getDataFromPDF(PDFS + "ACAN11-Fac.pdf")
    sendDataToDB(d)
    print("closing DB")
    db.close()