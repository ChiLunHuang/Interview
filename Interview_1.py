
#################################################
# Interview_1.py
#題目:給定wiki頁面，找出頁面中所有時間，並且以ISO8601日期格式印出並標出位置
#
# 2016 Chi-Lun Huang
#################################################
import requests
from bs4  import BeautifulSoup as bs
import jieba
from operator import itemgetter 
import dateutil.parser as parser
import re
import datetime

# Funtion for ISO8601 and output
def changeFormat(timeString,locationFirst,locationEnd,paragraphy) :

    try:
        text = timeString
        #print(text)
        date = (parser.parse(text))
        print('Date:',date.isoformat(),' ，Start:',locationFirst+1,'End:',locationEnd+1,' ，Original artical:',paragraphy,'\n')
    
    except:
        print ("") # 程》；隔/2/4 Date format is not correct.
        
        
    
# Funtion for processing chinese date    
def findDate(words) :
    
        
    for j in range(0,len(words)):
        #print(words[j].text)
            
        # 1.Chinese format
        # Find the words(年/月/日) in sentence
        if len (words) > 0 and ('年' in words[j].text and '月' in words[j].text and '日' in words[j].text):
            #print(words[j].text)
            paragraph = words[j].text
            for k in range (0,len(paragraph)):
                # Rebuilding chinese date
                if paragraph[k] == '年':
                    #print(paragraph[k-4:k])
                    # Month ex: 2, 4, 9 
                    if paragraph[k+2] == '月': 
                        #print(paragraph[k+1:k+2])
                        # Day ex: 3, 4, 7 
                        if paragraph[k+4] == '日': 
                            changeFormat(paragraph[k-4:k]+'/'+paragraph[k+1:k+2]+'/'+paragraph[k+3:k+4],k-4,k+4,paragraph)
                        # Day ex: 03, 04, 07 
                        elif paragraph[k+5] == '日':
                            changeFormat(paragraph[k-4:k]+'/'+paragraph[k+1:k+2]+'/'+paragraph[k+3:k+5],k-4,k+5,paragraph)

                    # Month ex: 02, 04, 09 
                    elif paragraph[k+3] == '月':
                        #print(paragraph[k+1:k+3])
                        # Day ex: 3, 4, 7 
                        if paragraph[k+5] == '日': 
                            changeFormat(paragraph[k-4:k]+'/'+paragraph[k+1:k+3]+'/'+paragraph[k+4:k+5],k-4,k+5,paragraph)
                        #Day ex: 03, 04, 07 
                        elif paragraph[k+6] == '日':
                            changeFormat(paragraph[k-4:k]+'/'+paragraph[k+1:k+3]+'/'+paragraph[k+4:k+6],k-4,k+6,paragraph)
        # 2.date format
        text = words[j].text

        match = re.search(r'\d{4}-\d{2}-\d{2}',text)
        match2 = re.search(r'\d{4}-\d{1}-\d{2}',text)
        match3 = re.search(r'\d{4}-\d{2}-\d{1}',text)
        match4 = re.search(r'\d{4}-\d{1}-\d{1}',text)

        if match  :
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date() 
            print('Date:',date.isoformat(),' ，From: 註釋內文;參考文獻',' ，Original artical:',text,'\n')

        elif match2 :
            date = datetime.datetime.strptime(match2.group(), '%Y-%m-%d').date() 
            print('Date:',date.isoformat(),' ，From: 註釋內文;參考文獻',' ，Original artical:',text,'\n')

        elif match3 :
            date = datetime.datetime.strptime(match3.group(), '%Y-%m-%d').date() 
            print('Date:',date.isoformat(),' ，From: 註釋內文;參考文獻',' ，Original artical:',text,'\n')

        elif match4 :
            date = datetime.datetime.strptime(match4.group(), '%Y-%m-%d').date() 
            print('Date:',date.isoformat(),' ，From: 註釋內文;參考文獻',' ，Original artical:',text,'\n')



        
        
# To get web content

res = requests.get(str(input("Please enter your url: ")))
soup = bs(res.text,'html.parser')



# Basic information
for infobox in soup.select('.infobox'):
    td = infobox.select('td')
    findDate(td)
    #print(td)

# Article   
for div in soup.select(".mw-content-ltr"):
    p = div.select('p')
    #print (p)
    findDate(p)

# Refrerence
for div in soup.select(".references"):
    referenceText = div.select(".reference-text")
    findDate(referenceText)
    
# wikitable
for div in soup.select(".wikitable"):
    tableText = div.select("td")
    findDate(tableText)
    
    


