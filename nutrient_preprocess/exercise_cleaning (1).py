#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('python -m pip install --upgrade pip')


# In[ ]:


get_ipython().system('pip install wordcloud')
get_ipython().system('pip install certifi --ignore-installed')


# In[ ]:


get_ipython().system('pip install jieba')


# In[ ]:


get_ipython().system('pip install googletrans')


# In[ ]:


get_ipython().system('mkdir jieba_data')


# In[ ]:


get_ipython().system('wget https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big -o jieba_data/dict.txt.big')


# In[ ]:


jieba.set_dictionary('jieba_data/dict.txt.big')


# In[ ]:


import time


# In[ ]:


import googletrans


# In[ ]:


from pprint import pprint


# In[ ]:


pprint(googletrans.LANGCODES) 


# In[ ]:


import random


# In[ ]:


from wordcloud import WordCloud


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


from PIL import Image


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import pymongo


# In[ ]:


import pandas as pd


# In[ ]:


import jieba


# In[ ]:


import re


# In[ ]:


import numpy as np


# In[ ]:


from collections import Counter


# In[ ]:


client = pymongo.MongoClient('192.168.158.128', 27017)


# In[ ]:


db = client.tibame


# In[ ]:


collection = db.recipe_raw


# In[ ]:


data = pd.DataFrame(list(collection.find()))
data


# In[ ]:


pd_ing = data['ingredient']


# In[ ]:


list_ing = []
for i in data['ingredient']:
    list_ing.append(i)
list_ing


# In[ ]:


list_steps = []
for i in data['steps']:
    list_steps.append(i)
list_steps


# # Data Merge

# In[ ]:


list_ing_merge = ''.join(str(list_ing[:2000]))
print(type(list_ing_merge))
list_ing_merge


# In[ ]:


list_steps_merge = ''.join(str(list_steps[:2000]))
print(type(list_steps_merge))
list_steps_merge


# In[ ]:





# # 中轉英

# In[ ]:


translator = googletrans.Translator()


# In[ ]:


results = translator.translate('我覺得今天天氣很差')
print(results)
print(results.text)


# In[ ]:





# In[ ]:





# In[ ]:


tra_list_ing = []
item = 1
for i in list_ing[:1000]:
    try:
        print(item)
        item += 1
        results = translator.translate(i)
        print(results.text)
        tra_list_ing.append(results.text)
        sleeptime=random.randint(3, 7)
        time.sleep(sleeptime)
        print('睡 %s 秒'%(sleeptime))
    except TypeError:
        pass
with open ('tra_list_ing.txt','w',encoding='utf-8') as t:
    t.write(str(tra_list_ing))
tra_list_ing


# In[ ]:


f = open ('mydict.txt','r',encoding='utf-8')
first_line = f.readlines()
print(first_line)


# In[ ]:


for i in first_line:
    results = translator.translate(i)
    print(results.text)
#         tra_dict.append(results.text)
    with open ('tra_mydict.txt','a',encoding='utf-8') as t:
        t.write(results.text+'\n')


# # 資料正規化

# In[ ]:


rdata = open('tra_list_ing.txt','r',encoding='utf-8')


# In[ ]:


# list_ing_fix =  re.sub('[*\dWA-Za-z/''\\\\]','',list_ing_merge)
# list_ing_fix1 =  re.sub('[*s,⋯⋯⋯⋯⋯⋯⋯⋯]','',list_ing_fix)
# list_ing_fix2 =  re.sub('[*｜（）()]','',list_ing_fix1)


# In[ ]:


first_line = rdata.readline()
second_line = rdata.readline()
print(first_line)
# print(second_line, first_line, sep = "\n")


# In[ ]:





# In[ ]:


regex_rdata =  re.sub('[\d,]','',first_line)
regex_rdata


# In[ ]:


list_ing_fix2


# In[ ]:


list_ing_fix1


# #  斷詞

# In[ ]:


split_rdata = regex_rdata.split()
split_rdata


# In[ ]:


list_ing_fix2


# In[ ]:


ing_words_list = jieba.lcut(list_ing_fix2)


# In[ ]:


ing_words_list


# # 保留字

# In[ ]:


with open(file='tra_mydict.txt',mode='r', encoding="UTF-8") as file:
    reserve_dict = file.readlines()
reserve_dict


# In[ ]:


re_reserve_words_list = []
for i in reserve_dict:
    results =  re.sub('[\s]','',i)
    re_reserve_words_list.append(results)
re_reserve_words_list


# # 食譜保留後數據

# In[ ]:


ing_words_list_reserveword = []
for term in split_rdata:
    if term in re_reserve_words_list:
        ing_words_list_reserveword.append(term)
ing_words_list_reserveword


# In[ ]:


ing_counter = Counter(ing_words_list_reserveword)
print(type(ing_counter))
ing_counter


# In[ ]:


ing_counter_sort = Counter(sorted(ing_words_list_reserveword))
ing_counter_sort


# # 停止字

# In[ ]:


stop_words_list = []
with open(file='stop_word.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        stop_words_list.append(line)
stop_words_list


# In[ ]:


ing_words_list = jieba.lcut(list_ing_fix2)
ing_words_list_stopword = []
for term in ing_words_list:
    if term not in stop_words_list:
        ing_words_list_stopword.append(term)
ing_words_list_stopword


# In[ ]:


ing_counter = Counter(ing_words_list_stopword)


# In[ ]:


ing_counter


# In[ ]:


ing_counter_1 = Counter(sorted(ing_words_list))


# In[ ]:


ing_counter_1


# In[ ]:


with open ('ing_counter.csv','w',encoding='utf-8') as f :
    f.write(str(ing_counter))


# In[ ]:





# # 文字雲

# In[ ]:


worldcloud = WordCloud(font_path='./fonts/TaipeiSansTCBeta-Regular.ttf').generate_from_frequencies(ing_counter)


# In[ ]:


plt.imshow(worldcloud, interpolation='bilinear')


# In[ ]:


plt.axis('off')


# In[ ]:





# In[ ]:


plt.show()


# In[ ]:


f = open(r'./test0916.txt',encoding='utf-8')


# In[ ]:


print(f.read())


# In[ ]:


queryArgs = {}
projectFeild = {'url' : True , 'ingredient': True}
search_response = db.recipe_raw.find(queryArgs,projectFeild)


# In[ ]:


recipe_lst = []
for item in search_response:
    try:
        recipe_lst.append(item['ingredient'])
    except Exception as error_name:
        print(error_name)
        pass


# In[ ]:


ingredient_str = ''
for item in recipe_lst:
    try:
        ingredient_str = ingredient_str + item
    except Exception as error_name:
        print(error_name)
        pass


# In[ ]:


print(type(ingredient_str))


# In[ ]:


queryArgs = {}
projectField = {'url' : True, 'title' : True, 'time' : True, 'author' : True, 'ingredient' : True, 'stpes' : True, 'comment' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)

print(type(search_response))

result_recipe = []
for n, item in enumerate(search_response):
    result_recipe.append(item)


# In[ ]:


result_recipe

