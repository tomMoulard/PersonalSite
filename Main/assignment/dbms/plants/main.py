# -*- coding: utf-8 -*-
"""
Created on Tue Apr 6 13:00:00 2017

@author: tm
To use the main program once
"""

print("Made by Tom Moulard")    

import getPDF
import putInDB
import shutil
    
CONFIG   = "./CONFIG"

def gettingCredsForDB():
    """
    Just used to gather configs (here just the path of the pdf folder)
    return PDFS
    """
    config   = open(CONFIG, "r")
    configs  = config.readlines()
    PDFS     = configs[12][:len(configs[12]) - 1]
    return PDFS

PDFS = gettingCredsForDB()

def main():
    getPDF.main()
    putInDB.main()
    print("Do you want to erase the pdf folder ? [y/N] ", end="")
    if (input() == "y"):
        print("erasing")
        shutil.rmtree(PDFS[:len(PDFS) - 1])
    print("Finished \nSee you later\nMade but Tom Moulard")

if __name__ == '__main__':
    main()