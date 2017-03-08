# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:08:13 2016

@author: Tom Moulard
"""

import urllib.request
opener = urllib.request.FancyURLopener({})
 
def cut2url2(src, debut="<img src=\"", end=".jpg\""):
    #to split the srt
    splited = src.split(debut)
    posInSplited, lSplited, res = 1, len(splited), []
    while posInSplited < lSplited:
        if ".jpg" in splited[posInSplited]:
            finded, pos, resTmp = False, 7, "http://"
            while not finded:
                while splited[posInSplited][pos] != ".":
                    resTmp += splited[posInSplited][pos]
                    pos += 1
                resTmp += splited[posInSplited][pos]
                pos += 1
                if splited[posInSplited][pos] == "j":
                    finded = True                
            res.append(resTmp + "jpg")
        posInSplited += 1
    return res
    
def cut2url3(src, debut="<img src=\"", end=".jpg\"(max 3 long)"):
    #to split the srt
    splited = src.split(debut)
    posInSplited, lSplited, res = 1, len(splited), []
    while posInSplited < lSplited:
        posInUrl, lUrl, resTmp = 0, len(splited[posInSplited]), ""
        notFound, prematureEnd = True, False
        while posInUrl < lUrl and notFound and not prematureEnd:
            if lUrl - posInUrl < 3:
                prematureEnd = True
            elif (
                splited[posInSplited][posInUrl]     == end[0] and
                splited[posInSplited][posInUrl + 1] == end[1] and
                splited[posInSplited][posInUrl + 2] == end[2]             
                  ):
                      notFound = False
            else:
                resTmp += splited[posInSplited][posInUrl]
            posInUrl += 1
        if not notFound: 
            resTmp += ".jpg"
            res.append(resTmp)
        posInSplited += 1
    return res
      


def generateUrl(keyWord):
    '''easier to generate 1st url'''
    return ("http://www.imposetonanonymat.com/page/"
            + keyWord) 


def getAllList(maxRange):
    print("Getting urls . . .")
    res = []
    for x in range(1, maxRange + 1):
        url = generateUrl(str(x))  
        responce = str(opener.open(url).read())
        urls = cut2url3(responce)
        for each in urls:
            res.append(each)
            if len(res) % 100 == 0:
                print("Got", str(len(res)), "Urls so far.")
    print("got urls")
    return res

#754 max
#tmp = getAllList(3)
#printList(tmp)
#print(len(tmp))
        
def makeADir():
    import os
    os.mkdir("C:/ITA/")

def download(urlList):
    print("downloading ...")
    import urllib
    pos, lUrlList = 0, len(urlList) 
    file = open("C:/ITA/README(urls).txt",'a')
    file.writelines("Made by Tom Moulard\nGot " + str(len(urlList)) + " Urls in total" + "\n")
    for x in urls:        
        file.writelines(str(pos + 1) + " " + urlList[pos] + "\n")
        pos +=1 
    file.close()
    pos = 0
    while pos < lUrlList:        
        print(pos, urlList[pos])
        link = "C:/ITA/" + str(pos + 1)+ ".jpg"
        urllib.request.urlretrieve(urlList[pos], link)
        pos += 1   
    print("finished")
    
#makeADir()    
inpu = int(input("How much pages to examine ? (max 754) ")) 
if inpu > 754 or inpu < 0:
    raise Exception ("You failed ! (Bad Input :/)")      
urls = getAllList(inpu)    
download(urls)  

print("Regarde le fichier \"C:\\ITA\\\"")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        