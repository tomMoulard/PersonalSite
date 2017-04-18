# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017
@python3
@author: tm
The goal is to send data to a db
data should be an array of tupple : ("<Name Of Column>","<Content To send>")
The DataBase with the credentials stored on the CONFIG file
V2

To use this:
import putInDB as pidb

#to use the db
pidb.goToDB()

#to use the table
pidb.goToTable(tableMeta)

#to send data
pidb.sendDataToDB(data, tableMeta)

#to close th connection
pidb.closeDB()
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
SN          = "16920041"
USER        = SN
SERVER      = "172.31.34.145"
PASSWORD    = SN
DB          = "db" + SN
CURSOR      = None;
CONFIG      = "./CONFIG"
PDFS        = "/tmp/plant_pdfs" 
TABLE       = "usdaplant"
PRIMARYKEYS = []

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
    TABLE = "usdaplant"
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

def printTable(tableMeta):
    """
    This is supposed to print the response of the db
    """
    exe("SELECT * FROM " + TABLE + ";")
    for col in tableMeta[:-1]:
        print(col[0], end=" -> ")
    print(tableMeta[-1][0])
    try:
        response = CURSOR.fetchall()
        for line in response:
            for words in line[:-1]:
                print(words, end=" -> ")
            print(line[-1])
        print("There is", len(response), "lines here")
    except:
        print("Failed to print DB response")
        print(sys.exc_info())


def changeColSize(colName, newSize, tableMeta):
    """
    This function change the colName size to newSize
    and update tableMeta
    """ 
    #get the pos in the tableMeta
    pos = 0
    for cols in range(len(tableMeta)):
        if colName == tableMeta[cols][0]:
            pos = cols
            break
    #getting the bigger value
    tableMeta[pos] =\
        (tableMeta[pos][0], tableMeta[pos][1], max(newSize, int(tableMeta[pos][2])))
    #setting the query
    val = "ALTER TABLE " + TABLE + " MODIFY " + tableMeta[pos][0] + " " +\
        tableMeta[pos][1] + "(" + str(tableMeta[pos][2]) + ");"
    exe(val)

def isAlreadyThere(primaryKey):
    """
    This check the db to know if the key is already there
    """
    return primaryKey in PRIMARYKEYS

def checkSizeAndModify(colName, size, tableMeta):
    """
    This is supposed to check if the column is big enought
    if not, just take nore space
    #By the way, the col should be in the table
    No return
    """
    #find colname in tableMeta and get this size
    pos = 0
    for col in range(len(tableMeta)):
        if colName == tableMeta[col][0]:
            pos = col
            break
    #if it is not big enought
    if int(tableMeta[pos][2]) < size:
        #update the table
        tableMeta[pos] = (tableMeta[pos][0], tableMeta[pos][1], str(size + 1))
        #and update the tableMeta
        changeColSize(colName, int(tableMeta[pos][2]), tableMeta)

def sendDataToDB(data, tableMeta):
    """
    This is used so select which data and who to send the to the db
    the table should be ready to accept data
    data format: [("<column name>", "<content>")]
    MUST PROVIDE tableMeta to get table informations
    [("<Col Name>", "<Col Type>", "<Col Size>")]
    if the symbol is already there just add the data from the pdf
    otherwise add all and and add primary key to PRIMARYKEYS
    """
    # create new columns
    for d in data:
        found = False
        for col in tableMeta:
            if d[0] == col[0]: # the col exist
                found = True
                break
        if not found:
            addCol(d[0], tableMeta, size=str(len(d[1]) + 1))
    #insert data
    #if already there just add 
    INS =  "INSERT INTO " + TABLE + "("
    if isAlreadyThere(data[0][1]):
        #USE DICT YOU DICK .....
        #Find "fs_Alternative_Name" and check his value
        if data[3][1] == "fs_Alternative_Name": #insert just 5/6
            checkSizeAndModify(data[5][0], len(data[d][1]), tableMeta)
            checkSizeAndModify(data[6][0], len(data[d][1]), tableMeta)
            INS = data[5][0]  + " " + data[6][0] +\
                ") WHERE " + data[0][0] + " = " + data[0][1] + \
                "VALUES ( "+ data[5][0]  + " " + data[6][0] + ");"
        else:
            checkSizeAndModify(data[3][0], len(data[d][1]), tableMeta)
            checkSizeAndModify(data[4][0], len(data[d][1]), tableMeta)
            INS = data[3][0]  + " " + data[4][0] +\
                ") WHERE " + data[0][0] + " = " + data[0][1] + \
                "VALUES ( "+ data[3][0]  + " " + data[4][0] + ");"
        exe(INS)
    else: #insert all the data
        VAL = ""
        for d in range(len(data[:-1])):
            INS += data[d][0] + ", "
            VAL += "\"" + data[d][1] + "\", "
            checkSizeAndModify(data[d][0], len(data[d][1]), tableMeta)
        INS += data[-1][0] + ") VALUES ("
        VAL += "\"" + data[-1][1] + "\");"
        exe(INS + VAL)
        #instert key in the PRIMARYKEYS array
        PRIMARYKEYS.append(data[0][1])
        #sendDataToDB(generateFakeData(), COLSMETA)

def addCol(colName, tableMeta, typeCols="VARCHAR", size="64"):
    """
    This symply add a new colone to the TABLE
    Called colName
    and update COLS
    """
    tableMeta.append((colName, typeCols, size))
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

def closeDB():
    """
    This is called to close the bd connexcion
    """
    db.close()

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
    for x in range(1, len(tableMeta)):
        CREATETABLE += ", " + tableMeta[x][0] + " " + tableMeta[x][1] +\
            "(" + str(tableMeta[x][2]) + ")"
    CREATETABLE += ") ENGINE=InnoDB; "
    exe(CREATETABLE)    

def main():
    goToDB()
    goToTable([])
    print("Table", TABLE, "Created")
    print("Opening pdfs parse them and store data in the db")
    files = glob.glob(PDFS + "*.pdf")
    for file in range(len(files)):
        print("getting data from", file[file])
        d = getDataFromPDF(files[file])
        sendDataToDB(d)
    exe("SHOW TABLES;")
    printTable()
    print("closing DB")
    db.close()