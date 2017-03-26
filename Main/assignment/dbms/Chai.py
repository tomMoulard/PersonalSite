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

def getLineCode(responce, pos):
    """
    Get the whole code from a box.
    The pos must be set just after the "crayon-code" (aka the begining of the box)
    return (line, newPos) as newPos an updated position is the responce
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
                        else:
                            line += responce[pos]
                            pos  += 1
                    line += " "
                    if "</span><span" != responce[pos:pos+12]:
                        pos  += 7
                        while pos < ll and responce[pos] != "<":
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
        pos += 1
    return code

def mainUrl(url):
    """
    Return any good urls on the page
    """
    responce = str(opener.open(url).read())
    urls = []
    pos  = 0
    ll   = len(responce)
    while pos < ll:
        #Iterate thru the whole responce to fill urls
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
    #Iterate thru all urls to get all code
    code = ["SHOW databases;"]
    db = MySQLdb.connect(SERVER, USER, PASSWORD, DB)
    print("Connected to server", SERVER, "with credential for :", USER)
    cursor = db.cursor()
    for x in range(len(urls)):
        print("getting code for", urls[x], "(", x, ")")
        tmp = getCodeFromUrl(urls[x])
        for y in tmp:
            bulk = random.randint(5, 20) * len(y)/200
            code.append(y)
            print(USER + "@" + SERVER + "(" + str(bulk) + ")" + "> " + y)
            try:
                cursor.execute(y)
            except:
                print(sys.exc_info()[0])
            time.sleep(bulk)
    #close the db
    db.close()

if __name__ == '__main__':
    main()