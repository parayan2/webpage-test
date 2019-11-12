import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sys
from flask import Flask, render_template, request
import os
import locale

app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
      return render_template('index.html')
    if request.method =='POST':
      plusurl= (request.form['Name'])
      page=5
      pageNum=1
      lastPage=int(page)*10-9
      
      list1=list()
      while pageNum < lastPage +1:

        baseurl = "https://search.naver.com/search.naver?where=article&sm=tab_jum&query=\""
        suburl ="\"중고나라%20판매중%20개인거래%28판매%29"
        addurl ="&prdtype=0&t=0&st=rel&date_option=0&date_from=&date_to=&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&board=&sm=tab_pge&start="
        url =  baseurl+urllib.parse.quote_plus(plusurl)+urllib.parse.quote_plus(suburl)+addurl+str(pageNum)

        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        my_price = soup.find_all(class_="cafe_item_price")
  
        for title in my_price:
            numbers = re.findall("\d+",title.text.replace(',',''))
            index=[]
            new_numbers=np.delete(numbers, index)
            real_numbers=int(new_numbers)
            list1.append(real_numbers)
            list1.sort() 

        pageNum += 10

      for i in range(0,len(list1)):
        locale.setlocale(locale.LC_ALL, '')
        list1[i]=locale.format('%3d', list1[i], 1) 
    list2={}
    for lst in list1:
      try: list2[lst] +=1
      except: list2[lst] =1 
    return render_template('index.html', list2=list2,plusurl=plusurl) 


if __name__=='__main__' :
    app.run(debug=True)   