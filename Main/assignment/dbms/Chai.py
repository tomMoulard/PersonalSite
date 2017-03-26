# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:07:26 2017

@author: tm
"""

#to get the http responce for files
import urllib.request
opener = urllib.request.FancyURLopener({})

#to get users imput
import sys

URL = "http://www.mysqltutorial.org/basic-mysql-tutorial.aspx"

def main():
        responce = str(opener.open(URL).read())
        #print(responce)
        print("Main Responce get")
        #curl link
        urls = []
        pos  = 0
        ll   = len(responce)
        while pos < ll:
            #Iterate thru the whole responce
            pos += 1
        print("links get")
        #Iterate thru all urls to get all code
        #connect to server
        #lauch code with random interval (5 - 20s between)


if __name__ == '__main__':
    main()