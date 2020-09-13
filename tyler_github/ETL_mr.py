# 司博特 目前抓取json ,txt已關閉
import requests
from bs4 import BeautifulSoup
import os
import csv
import json
import time
import random

headers = {}
ua = '''Referer: https://www.mr-sport.com.tw/weighttraining/page/2
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]] = i.split(": ")[1]
# 建立目標目錄及資料夾
resource_path = r'./mr_aerobic-training' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
resource_path = r'./mr_aerobic-training/json' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
# resource_path = r'./mr_aerobic-training/txt' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)

start = time.time()

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
            print(title_name)
            # 判斷是否已抓取過
            filepath = './mr_aerobic-training/json/%s.json' % (title_name)
            if os.path.isfile(filepath):
                print("gotcha")
                continue
            else:
                print("New for start")
            title_url = t.findAll('a')[0]['href']
            # print(title_url)
            url_2 = t.findAll('a')[0]['href']
            res_2 = requests.get(url_2, headers=headers)
            soup_2 = BeautifulSoup(res_2.text,'html.parser')
            article_1 = soup_2.select('div.entry')
            # print(article_1[0].text)
            content = article_1[0].text.split('※')[0]
            # print(article_1[0].text.split('※')[0])
            mr_json = []
            value = {'url': title_url, 'title': title_name, 'lesson': 0, 'lesson_time': 0,
                     'strengh': 0, 'describe': content, 'time': 0,'author': 0}
            mr_json.append(value)
            with open ('./mr_aerobic-training/txt/%s.txt'%(title_name),'w',encoding='utf-8') as f: ##需要修改
                f.write(title_name)
                f.write('\n')
                f.write(content)
                f.write('\n')
                f.write(title_url)
            transform_json_string = json.dumps(mr_json, ensure_ascii=False)
            # ensure_ascii=False (要加這個文字才不會變成數字)
            with open('./mr_aerobic-training/json/%s.json'%(title_name), 'w', encoding='utf-8') as j: ##需要修改
                j.write(transform_json_string)

        sleeptime=random.randint(3, 5)
        time.sleep(sleeptime)
        page +=1
if __name__ ==  '__main__':
    # 填入目標網址 以及 欲抓取頁數
    result = getArticle('https://www.mr-sport.com.tw/aerobic-training/page/%s',4) ##需要修改

end = time.time()
print('執行時間:%f 秒'%(end - start))