# ptt fitness  抓取json ,txt已關閉
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import pymongo
import random

# 建立目標目錄及資料夾
# resource_path = r'./ptt_fitness'
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./ptt_fitness/json' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./ptt_fitness/txt' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
###
client = pymongo.MongoClient('192.168.158.128', 27017)
db = client.tibame
collection = db.ptt_fitness
###
try:
    with open('./ptt_fitness/url_list.txt', 'a+', encoding='utf-8') as file:
        file.close()
except:
    pass

start = time.time()
#目標網址
url = 'https://www.ptt.cc/bbs/FITNESS/index%s.html'
headers = {}
ua ='''authority: www.ptt.cc
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]]=i.split(": ")[1]
    # print(i)




def savemongodb(value):
    insert_item = value
    insert_result = db.ptt_fitness.insert_one(insert_item)
    print(insert_result)



def getArticle(page):
    # 起始頁為 1
    pages = 266
    # 抓取每頁資訊
    for times in range(page):
        res = requests.get(url%(pages), headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        title = soup.select('div.title')
        print(pages)
        #print(title)
        # 抓取每頁資訊
        for t in title:
            try:
                title_name = t.findAll('a')[0].text
                tmp_a_tag = t.findAll('a')[0]
                title_url = 'https://www.ptt.cc' +t.findAll('a')[0]['href']
                #print(title_name)
                #print(tmp_a_tag)
                #print(title_url)
                url_2= 'https://www.ptt.cc' +t.findAll('a')[0]['href']
                #print(url_2)

                res_2 = requests.get(url=url_2, headers=headers)
                # print(res_2.text)
                soup_2 = BeautifulSoup(res_2.text,'html.parser')
                article = soup_2.select('div#main-content')
                article_time = soup_2.select('div.article-metaline')
                # print(article_time[2].text)
                # print(article)
                # print(article[0].text.split('--')[0])
                ###
                with open('./ptt_fitness/url_list.txt', 'r', encoding='utf-8') as f:
                    file = f.readlines()
                    url_list = []
                    for i in file:
                        result = i.replace('\n', '')
                        url_list.append(result)
                    if url_2 in url_list:
                        print('gotcca')
                        continue
                    else:
                        print('new')
                        value = {}
                        value['url'] = url_2
                        value['title'] = title_name
                        value['lesson'] = 0
                        value['lesson_time'] = 0
                        value['strengh'] = 0
                        value['describe'] = article[0].text.split('--')[0]
                        value['time'] = article_time[2].text
                        value['author'] = 0
                        savemongodb(value)

                        with open ('./ptt_fitness/url_list.txt','a',encoding='utf-8') as u:
                            out_str = url_2 + '\n'
                            u.write(out_str)

                    sleeptime_1 = random.randint(3,7)
                    time.sleep(sleeptime_1)
                    print('睡 %s 秒' % (sleeptime_1))
                        # insert_item = value
                        # insert_result = db.ptt_fitness.insert_one(insert_item)
                        # print(insert_result)

                        # fitness_json.append(value)
                        #
                        # fitness_json_string = json.dumps(fitness_json, ensure_ascii=False)
                        # # ensure_ascii=False (要加這個文字才不會變成數字)
                        # with open('./ptt_fitness/json/%s.json'%(title_name),'w', encoding='utf-8') as f:
                        #     f.write(fitness_json_string)

            except:
                pass


        pages += 1
        time.sleep(5)

if __name__ ==  '__main__':
    # 填入目標頁數
    result = getArticle(1477) ##需要修改


end = time.time()
print('執行時間:%f 秒'%(end - start))
print('finish')

