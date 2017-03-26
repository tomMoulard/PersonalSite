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

#mysql
#Please install python-mysqldb or python3-mysqldb before executing the script
import MySQLdb

URL = "http://www.mysqltutorial.org/basic-mysql-tutorial.aspx"

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
                            pos += 5
                        line += responce[pos]
                        pos  += 1
                    line += " "
                    if "</span><" != responce[pos:pos+8]:
                        pos  += 7
                        while pos < ll and responce[pos] != "<":
                            line += responce[pos]
                            pos  += 1
                        line += " "
                pos += 1
            if "</div>" == responce[pos:pos+6]:
                pos += 6
        if "</div>" == responce[pos:pos+6]:
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
            print("crayon-code")
            pos += 11
            line, pos = getLineCode(responce, pos)
            code.append(line)
        pos += 1
    return code

def main():
        print("Getting Main Responce")
        responce = str(opener.open(URL).read())
        #print(responce)
        print("Main Responce get")
        #curl link
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
        print("links get")
        #remove crappy urls
        urls = urls[3:len(urls) - 9]
        #Iterate thru all urls to get all code
        code = []
        for x in range(len(urls)):
            print("getting code for", urls[x], "(", x, ")")
            tmp = getCodeFromUrl(urls[x])
            for y in tmp:
                print(y)
                code.append(y)
        #connect to server
        db = MySQLdb.connect(SERVER, USER, PASSWORD, DB)
        print("Connected to server", SERVER, "with credential for :", USER)
        cursor = db.cursor()
        #cursor.execute("SELECT * FROM cities")
        #lauch code with random interval (5 - 20s between)
        for x in code:
            cursor.execute(x)
            print(USER + "@" + SERVER +"> " + x)
            time.sleep(random.randint(5, 25))
        #close the db
        db.close()

if __name__ == '__main__':
    main()