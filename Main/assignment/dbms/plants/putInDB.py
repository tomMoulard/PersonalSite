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

#Usefull stuff
import random
import time
import sys

#mysql
#Please install python-mysqldb or python3-mysqldb before executing the script
import MySQLdb

#PDF
#Please install PyPDF before executing the script
import PyPdf

