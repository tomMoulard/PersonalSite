
MORETOK = "https://plants.usda.gov/core/profile?symbol="
SYMBOL  = "ANHA"

import urllib.request
opener = urllib.request.FancyURLopener({})

import bs4 as bs

def prettyPrintForList(l):
    """
    This is a pretty print fo any list 
    """
    for x in range(len(l)):
        print(x, l[x])
    print("len(list)=", len(l))

def remove(l, c, lenC=1):
    """
    this remove the <c> char (on len <lenC>) from <l>
    Return l
    """ 
    res = ""
    pos = 0
    ll = len(l)
    while pos < ll:
        if l[pos:pos+lenC] != c:
            res += l[pos]
        else:
            pos += lenC - 1
        pos += 1
    return res

def yolo():
    res = [[]]
    mainresponse = str(opener.open(MORETOK + SYMBOL).read())
    if "No Data Found" in mainresponse:
        print("No Data Found")
    else:
        #data is situated here : <div id="content">DATA</div>
        soup = bs.BeautifulSoup(mainresponse, "lxml")
        greateDiv = soup.find("div", id="content")
        #This get all boardson the div delimited by an empty list
        greateDiv_row = greateDiv.find_all("tr")
        lastLab = "" #This is the last label
        pos = 0
        for tr in greateDiv_row:
            th = tr.find_all("th")
            lab =[i.text for i in th]
            lastLab = lab if lab else lastLab
            td = tr.find_all("td")
            row =[i.text for i in td]
            if not row: # New table
                res.append(lastLab)
                pos += 1
            else:
                res[pos].append(remove(row, "\\\t", 2))
        prettyPrintForList(res)

yolo()