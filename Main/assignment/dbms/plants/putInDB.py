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
#Please install python-mysqldb or python3-mysqldb before executing the script
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
        DB = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + "_" + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]) + "_" + "plants"
    #printnt("USER:", USER, "SERVER:", SERVER, "PASSWORD:", PASSWORD, "DB:", DB, "PDFS:", PDFS)
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

def getDataFromPDF(file):
    res = []
    raw = PyPDF2.PdfFileReader(file)
    rawer = ""
    #concatenate all the pages of the pdf in one string
    for pageNumber in range(raw.pages.lengthFunction()):
        rawer += raw.getPage(pageNumber).extractText() + "\n"
    raw.close()
    #let the parsing begin :3
    pos = 0
    ll = lent(rawer)
    while pos < ll:

        pos += 1
    return res

def sendDataToDB(data):
    """
    This is used so select which data and who to send the to the db
    the table should be ready to accept data
    """
    exe("SHOW databases;")

def main():
    print("Connected to server", SERVER, "with credential for :", USER)
    print("Opening pdfs parse them and store datas in the db")
    files = glob.glob(PDFS + "*.pdf")
    for file in files:
        data = getDataFromPDF(file)
        sendDataToDB(data)
    print("closing DB")
    db.close()