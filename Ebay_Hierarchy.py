# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 10:27:13 2019

@author: SAI
"""

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
d=dict()
fi=open("data_hierarchy1.csv","a+")
def fn(see,parent,strg,curr):

    url = see
    data = requests.get(url)
    soup = bs(data.text, features="html.parser")
    #print(parent,strg,curr)
    #print(soup.find_all('a',class_="b-textlink b-textlink--sibling"))
    siblings=[(i.text,i.get("href")) for i in soup.find_all('a',class_="b-textlink b-textlink--sibling")]
    parent1 = soup.find('a', class_='b-textlink b-textlink--parent').text
    #print(parent1,parent)

    for link in siblings:
            url = link[1]
            data = requests.get(url)
            soup = bs(data.text, features="html.parser")
            try:
                parent1=soup.find('a',class_='b-textlink b-textlink--parent').text
                #print(parent1)
                if(curr in d):
                    break
                if (parent1 == parent):
                    print(strg)
                    fi.write(strg)
                    fi.write("\n")
                    d[curr] = 1
                    break
                else:
                    #print(parent1,link[0])
                    fn(link[1],parent1,strg+'>'+link[0],link[0])
            except AttributeError:
                pass
            pass


url="https://www.ebay.com/v/allcategories"
data=requests.get(url)
soup = bs(data.text,features="html.parser")
music=soup.find('div',attrs={'class':'category-section','data-id':"Music"})
music_categories=music.findAll('div',class_="l1-name-wrapper")
#music_names=[i.find('h3',class_='ttl').text for i in music_categories]
#print(music_names)
music_names=[]
music_links=[i.find('a',class_='l1-name categories-with-links').get("href") for i in music_categories]
#print(music_links)
for i in music_links:
    url = i
    data = requests.get(url)
    soup = bs(data.text, features="html.parser")
    music_names.append(soup.find('span',class_='b-pageheader__text').text)
#print(music_names)
for i in range(len(music_links)):
    url = music_links[i]
    data=requests.get(url)
    soup = bs(data.text, features="html.parser")
    b_links=soup.findAll('li',class_="b-links-accordion")
    #print(b_links)
    seeall=[i.find('a',class_="b-textlink b-textlink--sibling").get("href") for i in b_links]
    seealltitles=[i.find('a',class_="b-textlink b-textlink--sibling").text.replace("See all in ","") for i in b_links]
    #print(seeall)
    k=soup.find('section',class_='b-module b-list b-speciallinks b-display--landscape')
    for nosee in k.find_all('a',class_="b-textlink b-textlink--parent"):
        p=nosee.get("href")
        q=nosee.text
        seeall.append(p)
        seealltitles.append(q)
    #print(seeall)
    #print(seealltitles)
    parent=music_names[i]
    for i in range(len(seeall)-1,-1,-1):

        fn(seeall[i],parent,parent+'>'+seealltitles[i],seealltitles[i])
#def fn(see,parent,strg,curr):
fi.close()
