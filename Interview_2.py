#################################################
# Interview_2.py
#題目:給定wiki頁面，找出頁面中所有的人名以及出現頻率
#
# 2016 Chi-Lun Huang
#################################################


import requests
from bs4  import BeautifulSoup as bs
import jieba
import jieba.posseg as pseg
from operator import itemgetter #sort

# To get web content
res = requests.get(str(input("Please enter your url: ")))
soup = bs(res.text.encode('utf8'),'html.parser')
#initialize
jieba.initialize()
# Add traditional chinese dictionary in jieba
#jieba.set_dictionary('dict.txt.big.txt')
# Add dictionary some words to recognize some words which recognize error in jieba
jieba.load_userdict("userdict.txt")

global dic
dic = {}
  
# function for jieba process
def jiebaProcess(words) :
    for i in range(0,len(words)): 
            seg = words[i].text
            if len(seg) > 0 :
                #print(seg) #Original file 
                seg_paragraph = seg.split('。')
                # read seg_paragraph
                for j in range(0,len(seg_paragraph)) :
                    #print(seg_paragraph[j]) # Original seg_paragraph

                    if len(seg_paragraph[j]) > 0 :
                        # Use jiebia to get POS 
                        segmented_result = pseg.cut(str(seg_paragraph[j]))
                        for pos in segmented_result:
                            #print (pos.word, pos.flag)
                            # Add result into dic        
                            if pos.word not in dic and pos.flag =='nr' and len(pos.word)>1:
                                dic[pos.word] = 1
                                #print (pos.word, pos.flag) # Result
                                    
                            elif pos.word in dic and pos.flag =='nr'and len(pos.word)>1:
                                dic[pos.word] += 1

                                                                                                
# Basic information
for infobox in soup.select('.infobox'):
    td = infobox.select('td')
    jiebaProcess(td)
       

# Article   
for div in soup.select(".mw-content-ltr"):
    p = div.select('p')
    jiebaProcess(p)
    
# Refrerence
for div in soup.select(".references"):
    referenceText = div.select(".reference-text")
    jiebaProcess(referenceText)   

# wikitable
for div in soup.select(".wikitable"):
    tableText = div.select("td")
    jiebaProcess(tableText)    

#Result
swd = sorted(dic.items(), key=itemgetter(1), reverse=True)
print (swd)

#D:\Anaconda3\Lib\site-packages\jieba
