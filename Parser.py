import numpy as np
import os,re
from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
import SOM
from Visualisation import makeAdotsOrig
Geo = []
ma = MA()
st = PST()
wt = WPT()
def realonlycoord():
    realfilecoord = open('coordReal.txt', 'r', encoding='utf-8')
    coord=[]
    temp = []
    k=0
    for line in realfilecoord:

        if k==3:
            temp[0] = ((temp[0]+180)*2)/(180+180)-1
            temp[1] = ((temp[1]+90)*2)/(90+90)-1
            coord+=[temp]
            k=0
            temp=[]
        elif k!=0:
            temp+=[float(line)]
        k+=1
    coord+=[temp]
    realfilecoord.close()
    return coord
def processingText(DirOn, poem, poemDir, Geo ):
    if DirOn:
        with open(poemDir, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        poem = "http://lib.ru/INPROZ/" + poem
        text = BS(get(poem).content).text
        print(text)
        my_file = open(poemDir, "w", encoding='utf-8')
        my_file.write(text)
        my_file.close()

    text_=st.sentences_from_text(text)
    for sent in text_:
        for word in wt.tokenize(sent):
            for morph in ma.parse(word):
                if "Geox" in morph.tag and morph.score>=0.3:
                    if morph.normal_form not in Geo:
                        #Geo += [[morph.normal_form, morph.score]]
                        Geo+=[morph.normal_form]
    #print(Geo)
    #print(len(Geo))

def filenotfound():
    home = 'texts/'
    link = "http://lib.ru/INPROZ/"
    soup = BS(get(link).content)
    b = soup.find('li')
    #testik = True
    while 1:
        try:
            b2 = b.find('a')
        except AttributeError:
            break
        #print(b2['href'])
        author = re.sub('/','',b2['href'])
        DirOn = False
        if author.find('http') != -1 or author.find('..') != -1:
            b = b.nextSibling
            continue

        try:
            temp = home+author
            os.mkdir(temp)
        except FileExistsError:
            DirOn = True

        link2 = link+b2['href']

        soup2 = BS(get(link2).content)
        t = soup2.find('li')
        bool2 = True
        while bool2:

            try:
                t2 = t.find('a')
                poem =  re.sub('_Contents','',t2['href'])
                poemDir = home + author + '/' + poem
                poem = author + '/' + poem
                if poemDir.find('http') != -1:
                    t = t.nextSibling
                    continue
                processingText(DirOn, poem, poemDir, Geo)
                t = t.nextSibling
            except AttributeError:
                bool2 = False
            except TypeError:
                bool2 = False
            except OSError:
                bool2 = False

        b = b.nextSibling
try: #беру гео слова из файла
    geofile = open('geox.txt', 'r', encoding='utf-8')
    Geo = [line.strip() for line in geofile]
    #print(Geo)
except FileNotFoundError: # файла нет - провожу обработку и записываю слова в файл
    print('file not found')
    filenotfound()
    Geo.sort()
    geofile = open('geox.txt', "w", encoding='utf-8')
    for i in Geo:
        geofile.write(i+'\n')
    geofile.close()

GeoD={}
coord=[]


try: #считываю координаты из файла
    geocoord = open('coord.txt','r', encoding='utf-8')
    coord=[]
    temp = []
    k=0
    for line in geocoord:
        #print(float(line))
        if k==2:
            coord+=[temp]
            k=0
            temp=[]
        temp+=[float(line)]
        k+=1
    coord+=[temp]
except FileNotFoundError:#координат нет - гуглю и записываю в файл
    wiki='https://ru.wikipedia.org/wiki/'
    geocoord_Real = open('coordReal.txt', "w", encoding='utf-8')
    for i in Geo:
        #print(i)
        wikiGeo = ''
        wikiGeo = wiki + i
        try: # пытаемся вытянуть координату из вики
            text = BS(get(wikiGeo,timeout=10).content)
            t = text.find('a','mw-kartographer-maplink')
            y = float(t['data-lat'])
            x = float(t['data-lon'])
            geocoord_Real.write(i+'\n')
            geocoord_Real.write(str(x)+'\n')
            geocoord_Real.write(str(y)+'\n')
        except  TypeError:# не смог - задаю рандомные
            x=float(np.random.uniform(-180, 180, 1))
            y=float(np.random.uniform(-90, 90, 1))

        x=((x+180)*2)/(180+180)-1
        y=((y+90)*2)/(90+90)-1
        X=[x,y]
        coord+=[X]
        GeoD.update({i:X})
    geocoord_Real.close()
    geocoord = open('coord.txt', "w", encoding='utf-8')
    for i in coord:
        for j in i:
            geocoord.write(str(j)+'\n')
    geocoord.close()
"""
coord = realonlycoord()
"""
makeAdotsOrig(coord)
SOM.test_som_with_color_data(coord)
