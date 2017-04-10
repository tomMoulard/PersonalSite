# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:00:00 2017

@author: tm

The goal is to save in the date.txt file the current date like:
[Date.UTC(<year>,<month>,<day>),<value>],
"""

import time
import os

FILE = "./date.txt"

def mergeList(l):
    """
    This function is supposed to merge all strings in the list
    return this merged string
    """
    res = ""
    for x in l:
        res += x
    return res

def main():
    #set the new date
    t       = time.localtime()
    message = "[Date.UTC("
    message += str(t[0])  + "," +\
        str(t[1]) + "," +\
        str(t[2]) + ")," +\
        str(t[5]) + "]"
    #open the file and read content
    f    = open(FILE, "r")
    data = f.read()
    #close and delete the file
    f.close()
    os.remove(FILE)
    #inserting the actual date in the previous file
    splitedData     = data.split("\n")
    splitedData[-1] = message
    splitedData[-2] = splitedData[-2] + ", "
    for line in range(len(splitedData)):
        splitedData[line] += "\n"
    splitedData.append("]);")
    #creating the new file and write datas
    f = open(FILE, "a")
    f.write(mergeList(splitedData))
    f.close()

if __name__ == '__main__':
    main()