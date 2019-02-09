# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:07:25 2019

@author: SAI
"""

import csv
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
my_url="https://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&ftab=AllFeedback&userid=littlekitty0103&iid=-1&de=off&items=25&interval=0&searchInterval=30&mPg=54&page=1"
uclient=ureq(my_url)
page_html=uclient.read()
uclient.close()
page_soup=soup(page_html,"html.parser")
total_pages=page_soup.find("b",{"class":"pg-num"})
total=''
arr=list(total_pages.text)
for i in range(len(arr)):
    if(arr[i].isnumeric()==False):
        i+=1
        while(arr[i].isnumeric()==False):
            i+=1
        while(i<len(arr)):
            total=total+arr[i]
            i+=1
        break
products=[]
cost=[]
feedback=[]
for new in range(1,3):
    my_url="https://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&ftab=AllFeedback&userid=littlekitty0103&iid=-1&de=off&items=25&interval=0&searchInterval=30&mPg=54&page="+str(new)
    uclient=ureq(my_url)
    page_html=uclient.read()
    uclient.close()
    
    page_soup=soup(page_html,"html.parser")
    temp=page_soup.findAll("tr",{"class":"bot"})
    for i in range (0,len(temp)):
        le=temp[i].findAll("td")
        product=le[1].text
        price=le[2].text 
        products.append(product)      
        cost.append(price)  
    table_body=page_soup.find('table',{'class':'FbOuterYukon'})    
    trows=table_body.findAll("tr")   
    for k in range (len(trows)):       
        ex=trows[k].findAll("td")
        
        if(len(ex)==1):
            break
        if(k%2!=0):
            
            feedback.append(ex[1].text)
    for l in range(k,len(trows)):
        te=trows[l].findAll("td")
        if(l%2==0):
            feedback.append(te[1].get_text())
            
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="123456789")
mycursor=mydb.cursor()
mycursor.execute("CREATE DATABASE CRAWLER")
mycursor.execute("USE CRAWLER")
mycursor.execute("CREATE TABLE WEBCRAWLER(product_no int AUTO_INCREMENT PRIMARY)")
for i in range(len(products)):
    sql="INSERT INTO WEBCRAWL1(PRODUCT, COST, FEEDBACK) VALUES(%s, %s, %s)" 
    values=(products[i],cost[i],feedback[i])
    mycursor.execute(sql,values)
    mydb.commit()