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
res = requests.get("https://zh.wikipedia.org/wiki/%E5%8F%B0%E7%81%A3%E7%A9%8D%E9%AB%94%E9%9B%BB%E8%B7%AF%E8%A3%BD%E9%80%A0%E5%85%AC%E5%8F%B8")
soup = bs(res.text.encode('utf8'),'html.parser')


# Add traditional chinese dictionary in jieba
jieba.set_dictionary('dict.txt.big.txt')
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
                            # Add result into dic        
                            if pos.word not in dic and pos.flag =='nr' and len(pos.word)>1:
                                dic[pos.word] = 1
                                #print (pos.word, pos.flag) # Result
                                    
                            elif pos.word in dic and pos.flag =='nr'and len(pos.word)>1:
                                dic[pos.word] += 1

                                                                                                
# Basic information
for vcard in soup.select('.vcard'):
    td = vcard.select('td')
    jiebaProcess(td)
       

# Article   
for div in soup.select(".mw-content-ltr"):
    p = div.select('p')
    jiebaProcess(p)
    
# Refrerence
for div in soup.select(".references-small"):
    referenceText = div.select(".reference-text")
    jiebaProcess(referenceText)   
    

#Result
swd = sorted(dic.items(), key=itemgetter(1), reverse=True)
print (swd)