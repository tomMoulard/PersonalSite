# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:00:00 2017

@author: tm
"""

#credentials
#mysql -u 16920041 -h 172.31.34.145 -p
SN       = "16920041"
USER     = SN
SERVER   = "172.31.34.145"
PASSWORD = SN
DB       = "db" + SN

#to get the http responce for files
import urllib.request
opener = urllib.request.FancyURLopener({})

#Random
import random
import time
import sys

#mysql
#Please install python-mysqldb or python3-mysqldb before executing the script
import MySQLdb

URLS = [
"http://www.mysqltutorial.org/basic-mysql-tutorial.aspx",
"http://www.mysqltutorial.org/mysql-stored-procedure-tutorial.aspx",
"http://www.mysqltutorial.org/mysql-triggers.aspx",
"http://www.mysqltutorial.org/mysql-views-tutorial.aspx",
"http://www.mysqltutorial.org/mysql-functions.aspx"
]

def swappInList(l, pos1, pos2):
    """
    Just swapp the l[pos1] and l[pos2] in the list
    For a Cleaner code purpose
    """
    l[pos1], l[pos2] = l[pos2], l[pos1]

def shuffleList(l):
    """
    This function is straight forward, it just shuffle the list using Random
    Does not return the list, it changes it directly
    """
    ll = len(l)
    for x in range(ll):
        swappInList(l, x, random.randint(0, ll))


def parseCode(code):
    """
    This function is used to parse and correct the line to make a proper statement (hopefully)
    return the right code to execute
    """
    return code

def getLineCode(responce, pos):
    """
    Get the whole code from a box.
    The pos must be set just after the "crayon-code" (aka the beginning of the box)
    return (line, newPos) as newPos an updated position is the response
    """
    line = ""
    ll = len(responce)
    while pos < ll: 
        if "crayon-line" == responce[pos:pos+11]:
            pos += 11
            while pos < ll and "</div>" != responce[pos:pos+6]:
                if "<span" == responce[pos:pos+5]:
                    while pos < ll and responce[pos] != ">":
                        pos += 1
                    pos += 1
                    while pos < ll and responce[pos] != "<":
                        if "&nbsp;" == responce[pos:pos+6]:
                            pos += 6
                        elif "  " == responce[pos:pos+2]:
                            pos += 3
                        elif "\\" == responce[pos]:
                            pos += 2
                        else:
                            line += responce[pos]
                            pos  += 1
                    line += " "
                    if "</span><span" != responce[pos:pos+12]:
                        pos  += 7
                        while pos < ll and responce[pos] != "<":
                            if "&nbsp;" == responce[pos:pos+6]:
                                pos += 6
                            elif "\\" == responce[pos]:
                                pos += 2
                            elif "  " == responce[pos:pos+2]:
                                pos += 2
                            else:
                                line += responce[pos]
                                pos  += 1
                        line += " "
                pos += 1
        if "</div></div>" == responce[pos:pos+12]:
            break
        pos += 1
    return line, pos

def getCodeFromUrl(url):
    """
    Get the whole code from the page
    return an array of all the code on dat page
    """
    responce = str(opener.open(url).read())
    code = []
    pos = 0
    ll = len(responce)
    while pos < ll:
        if "crayon-code" == responce[pos:pos+11]:
            pos += 11
            line, pos = getLineCode(responce, pos)
            #print(len(code), ":", line)
            if "USE" != line[:3]:
                code.append(line)
            if not ";" in line[len(line) - 10:]:
                line += ";"
            if ("|" in line) or ("]" in line) or ("..." in line):
                line = "" 
        pos += 1
    return parseCode(code)

def mainUrl(url):
    """
    Return any good urls on the page
    """
    responce = str(opener.open(url).read())
    urls = []
    pos  = 0
    ll   = len(responce)
    while pos < ll:
        #Iterate thru the whole response to fill urls
        if "<article" == responce[pos:pos+8]:
            #inside the right container
            while pos < ll:
                if "</article" == responce[pos:pos+9]:
                    #out of the right container
                    break
                else:
                    if "http://www.mysqltutorial.org/" == responce[pos:pos+29]:
                        #This is a link in the page
                        zelda = ""
                        while pos < ll and responce[pos] != "\"":
                            zelda += responce[pos]
                            pos += 1
                        urls.append(zelda)
                pos +=1
        pos += 1
    #remove crappy urls
    urls = urls[:len(urls) - 9]
    return urls


def main()  :
    print("Welcome \nThis is made by Tom MOULARD\nhttp://tom.moulard.org/")
    print("Just Configure your credentials inside the file if not aready did")
    print("Getting Links", end=" ")
    urls = []
    for lru in URLS:
        tmp = mainUrl(lru)
        for x in tmp:
            urls.append(x)
    print("OK (" + str(len(urls)) + ")")
    shuffleList(urls)
    print("urls shuffled")
    #Iterate thru all urls to get all code
    code = ["SHOW databases;"]
    db = MySQLdb.connect(SERVER, USER, PASSWORD, DB)
    print("Connected to server", SERVER, "with credential for :", USER)
    cursor = db.cursor()
    for x in range(len(urls)):
        print("getting code for", urls[x], "(", x, ")")
        tmp = getCodeFromUrl(urls[x])
        for line in tmp:
            bulk = random.randint(5, 20) * len(line) / 200
            #bulk = len(line) * random.random() / 1.5
            code.append(line)
            print(USER + "@" + SERVER + "(" + str(bulk) + ")" + "> " + line)
            try:
                cursor.execute(line)
            except:
                print(sys.exc_info()[0])
            time.sleep(bulk)
    #close the db
    db.close()

if __name__ == '__main__':
    main()