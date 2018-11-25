from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
import os,re
Geo = {}
ma = MA()
st = PST()
wt = WPT()
def processingText(DirOn, poem, poemDir ):
    if DirOn:
        with open(poemDir, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        #print("POEM ",poem)
        poem = "http://lib.ru/INPROZ/" + poem
        text = BS(get(poem).content).text
        print(text)
        my_file = open(poemDir, "w", encoding='utf-8')
        my_file.write(text)
        my_file.close()

    text_=st.sentences_from_text(text)
    #print(text_[30])
    #lenS=len(text_)
    #print(lenS)
    #Geo = {}
    for sent in text_:
        for word in wt.tokenize(sent):
            for morph in ma.parse(word):
                if "Geox" in morph.tag and morph.score>=0.3:
                    #print(word, morph)
                    if morph.normal_form not in Geo:
                        #Geo += [[morph.normal_form, morph.score]]
                        Geo.update({morph.normal_form:[#morph.tag,
                        morph.score]})
                        #Geo +=[morph.normal_form]
    print(Geo)
    print(len(Geo))


home = 'texts/'
link = "http://lib.ru/INPROZ/"
soup = BS(get(link).content)
b = soup.find('li')
while 1:
    b2 = b.find('a')
    #print(b)
    #print(b['href'])
    #print(soup.find('a'))
    print(b2['href'])
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
    #print(link2)

    soup2 = BS(get(link2).content)
    t = soup2.find('li')
    bool2 = True
    while bool2:

        try:
            t2 = t.find('a')
            #print(t2['href'],"what")
            poem =  re.sub('_Contents','',t2['href'])
            poemDir = home + author + '/' + poem
            poem = author + '/' + poem
            #print("GEWGWGW ", poemDir)
            if poemDir.find('http') != -1:
                t = t.nextSibling
                continue
            processingText(DirOn, poem, poemDir)
            t = t.nextSibling
        except AttributeError:
            bool2 = False
        except TypeError:
            bool2 = False
        except OSError:
            bool2 = False

    b = b.nextSibling
