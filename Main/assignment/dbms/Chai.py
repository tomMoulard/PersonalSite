# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:07:26 2017

@author: tm
"""

#to get the http responce for files
import urllib.request
opener = urllib.request.FancyURLopener({})

#Random
import random

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
                        line += responce[pos]
                        pos  += 1
                pos += 1
        if "</div>" == responce[pos:pos+6]:
            break
        pos += 1
    print(pos)
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
            print("code get :", tmp)
            for y in tmp:
                code.append(y)
                print(y)
        #connect to server
        #lauch code with random interval (5 - 20s between)


if __name__ == '__main__':
    main()