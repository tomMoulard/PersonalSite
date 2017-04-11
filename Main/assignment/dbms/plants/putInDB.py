# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm
The goal is to send data to a db
data should be an array of tupple : ("<Name Of Column>","<Content To send>")
The DataBase with the credentials stored on the CONFIG file
V2
"""


#Usefull stuff
import random
import time
import sys

#mysql
#Please install python-mysqldb 
#or python3-mysqldb before executing the script
import MySQLdb

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
    config.close()
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
print("Connected to server", SERVER, "with credential for :", USER)

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
    NEED TO BE REDONE :/
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

def goToDB():
    """
    This is used to CREATE or USE the DB
    a login phase like
    """
    try :
        exe("CREATE DATABASE IF NOT EXISTS " + DB + ";")
    except:
        print("Database is existent")
    try:
        exe("USE " + DB +";")
    except:
        print("already using database ?")

def goToTable(tableMeta):
    """
    This startup the table to correct from the begining
    Use the tableMeta form
    Should be an array and each col of this array represent a col
    in the DB and the first is the PRIMARY KEY and is NOT NULL
    Each cell should be like: ("<Col Name>", "<Col Type>", "<Col Size>")
    like [("Symbol", "VARCHAR", "10")]
    """
    CREATETABLE = """
        DROP TABLE IF EXISTS """ + TABLE + """;
        CREATE TABLE """ + TABLE + "( "
    #Adding the primary key
    CREATETABLE += tableMeta[0][0] + " " + tableMeta[0][1] +\
            "(" + tableMeta[0][2] + ") PRIMARY KEY NOT NULL"
    #adding all knowned columns
    for x in range(1, len(data)):
        CREATETABLE += ", " + tableMeta[x] + " = " + tableMeta[x]
    CREATETABLE += ") ENGINE=InnoDB"
    exe(CREATETABLE)    

def main():
    print("Table", TABLE, "Created")
    print("Opening pdfs parse them and store data in the db")
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", file[file])
        d = getDataFromPDF(files[file])
        sendDataToDB(d)
    print("closing DB")
    db.close()