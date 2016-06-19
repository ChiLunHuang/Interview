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

    text = timeString
    date = (parser.parse(text))
    print('Date:',date.isoformat(),' ，Start:',locationFirst+1,'End:',locationEnd+1,' ，Original artical:',paragraphy,'\n')
    
# Funtion for processing chinese date    
def findDate(words,classify) :
    # Block1 (Basic information and Article)
    if classify == '1' :
        for j in range(0,len(words)):
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
    #Block2 (Refrerence)
    elif classify == '2' :
        # Use regular expression to recognize date
        for o in range(0,len(words)): 
            text = words[o].text

            match = re.search(r'\d{4}-\d{2}-\d{2}',text)
            match2 = re.search(r'\d{4}-\d{1}-\d{2}',text)
            match3 = re.search(r'\d{4}-\d{2}-\d{1}',text)
            match4 = re.search(r'\d{4}-\d{1}-\d{1}',text)

            if match  :
                date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date() 
                
            elif match2 :
                date2 = datetime.datetime.strptime(match2.group(), '%Y-%m-%d').date() 
                
            elif match3 :
                date3 = datetime.datetime.strptime(match3.group(), '%Y-%m-%d').date() 
                
            elif match4 :
                date4 = datetime.datetime.strptime(match4.group(), '%Y-%m-%d').date() 
                   
            #result 
            print('Date:',date.isoformat(),' ，From: 註釋內文',' ，Original artical:',text,'\n')
        
        
        
# To get web content
res = requests.get("https://zh.wikipedia.org/wiki/%E5%8F%B0%E7%81%A3%E7%A9%8D%E9%AB%94%E9%9B%BB%E8%B7%AF%E8%A3%BD%E9%80%A0%E5%85%AC%E5%8F%B8")
soup = bs(res.text,'html.parser')



# Basic information
for vcard in soup.select('.vcard'):
    td = vcard.select('td')
    findDate(td,'1')    

# Article   
for div in soup.select(".mw-content-ltr"):
    p = div.select('p')
    findDate(p,'1')

# Refrerence
for div in soup.select(".references-small"):
    referenceText = div.select(".reference-text")
    findDate(referenceText,'2')
