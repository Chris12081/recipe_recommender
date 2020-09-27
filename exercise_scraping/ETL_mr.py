# 司博特 目前抓取json ,txt已關閉
import requests
from bs4 import BeautifulSoup
import os
import csv
import json
import time
import random
import pymongo


headers = {}
ua = '''Referer: https://www.mr-sport.com.tw/weighttraining/page/2
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]] = i.split(": ")[1]
# 建立目標目錄及資料夾
# resource_path = r'./mr_aerobic-training' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./mr_aerobic-training/json' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./mr_aerobic-training/txt' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)

client = pymongo.MongoClient('192.168.158.128', 27017)
db = client.tibame
collection = db.ptt_fitness

try:
    with open('./mr_aerobic-training/url_list.txt', 'a+', encoding='utf-8') as file:
        file.close()
except:
    pass

start = time.time()

def savemongodb(value):
    insert_item = value
    insert_result = db.mr_aerobic.insert_one(insert_item)
    print(insert_result)

def getArticle(url,pages): ##需要修改
    # 起始page 從1開始
    page = 1
    # url = 'https://www.mr-sport.com.tw/weighttraining/page/%s'
    # headers = {}
    # ua = '''Referer: https://www.mr-sport.com.tw/weighttraining/page/2
    # User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'''
    for i in ua.split("\n"):
        headers[i.split(": ")[0]] = i.split(": ")[1]
    # 抓取每頁資訊
    for times in range(pages):
        res = requests.get(url%(page), headers=headers)
        # print(res)
        soup = BeautifulSoup(res.text,'html.parser')
        # print(soup)
        title = soup.select('h2')
        # print(title[0].text)
        # 抓取每篇文章
        for t in title:
            title_name = t.findAll('a')[0].text
            # print(title_name)

            title_url = t.findAll('a')[0]['href']
            # print(title_url)
            url_2 = t.findAll('a')[0]['href']
            with open('./mr_aerobic-training/url_list.txt', 'r', encoding='utf-8') as f:
                file = f.readlines()
                url_list = []
                for i in file:
                    result = i.replace('\n', '')
                    url_list.append(result)
                if  title_url in url_list:
                    print('gotcca')
                    continue
                else:
                    print('new')
                    res_2 = requests.get(url_2, headers=headers)
                    soup_2 = BeautifulSoup(res_2.text,'html.parser')
                    article_1 = soup_2.select('div.entry')
                    # print(article_1[0].text)
                    content = article_1[0].text.split('※')[0]
                    # print(article_1[0].text.split('※')[0])
                    value = {}
                    value['url'] = title_url
                    value['title'] = title_name
                    value['lesson'] = 0
                    value['lesson_time'] = 0
                    value['strengh'] = 0
                    value['describe'] = content
                    value['time'] = 0
                    value['author'] = 0
                    savemongodb(value)
                    with open('./mr_aerobic-training/url_list.txt', 'a', encoding='utf-8') as u:
                        out_str = title_url + '\n'
                        u.write(out_str)

            # with open ('./mr_aerobic-training/txt/%s.txt'%(title_name),'w',encoding='utf-8') as f: ##需要修改
            #     f.write(title_name)
            #     f.write('\n')
            #     f.write(content)
            #     f.write('\n')
            #     f.write(title_url)
            # transform_json_string = json.dumps(mr_json, ensure_ascii=False)
            # # ensure_ascii=False (要加這個文字才不會變成數字)
            # with open('./mr_aerobic-training/json/%s.json'%(title_name), 'w', encoding='utf-8') as j: ##需要修改
            #     j.write(transform_json_string)

        sleeptime=random.randint(3, 5)
        time.sleep(sleeptime)
        page +=1
if __name__ ==  '__main__':
    # 填入目標網址 以及 欲抓取頁數
    result = getArticle('https://www.mr-sport.com.tw/aerobic-training/page/%s',4) ##需要修改

end = time.time()
print('執行時間:%f 秒'%(end - start))