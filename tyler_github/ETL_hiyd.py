# hiyd
import requests
from bs4 import BeautifulSoup
import os
import csv
import json
import time
import random
from opencc import OpenCC
import math
from urllib.parse import urlparse



# 將簡轉繁
str =OpenCC('s2t')
#print(str.convert(file))

#目標網址
url = 'https://www.hiyd.com/bb/?page=%s'
headers={}
ua = '''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36
Referer: https://www.hiyd.com/bb/
# Connection: keep-alive
# Cookie: _webp=1; coach_gender=1; Hm_lvt_27e0b89fc1f2e9d960a18d82d5f98dbd=1598705109,1598886716,1599149346,1599198467; Hm_lpvt_27e0b89fc1f2e9d960a18d82d5f98dbd=1599235292
# Host: www.hiyd.com'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]] = i.split(": ")[1]

# 建立目標目錄及資料夾
resource_path = r'./hiyd' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
resource_path = r'./hiyd/hiyd_txt' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
resource_path = r'./hiyd/hiyd_json' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)





start = time.time()

def getArticle(page):
    pages = 1


    for times in range(page):  #pages
        res = requests.get(url%(pages), headers=headers)
        print('目前在第%s頁'%(pages))
        # print(res)
        soup = BeautifulSoup(res.text,'html.parser')
        # print(soup)
        title = soup.select('h2')
        # print(title[0].text)

        for t in title:
            title_name = t.findAll('a')[0].text
            title_name_1 = str.convert(title_name)

            print(str.convert(title_name))
            filepath = './hiyd/hiyd_json/%s.json' % (title_name_1).replace('/','_')
            if os.path.isfile(filepath):
                print("gotcha")
                continue
            else:
                print("New for start")
            print('---')
            title_url = 'https://'+ t.findAll('a')[0]['href'][2:]
            # print(title_url)
            # print('---')
            url_2 = 'https:'+ t.findAll('a')[0]['href']
            res_2 = requests.get(url_2, headers=headers)
            soup_2 = BeautifulSoup(res_2.text,'html.parser')
            # print(soup_2.text)
            time_strengh = soup_2.select('div.hd-row2')
            time_strengh_1 = str.convert(time_strengh[0].text)
            time_strengh_2 = time_strengh_1.split()
            # print(time_strengh_2)
            times = time_strengh_2[1]
            print(times)
            strengh = time_strengh_2[2].split('：')
            print(strengh[1])

            # print(str.convert(time_strengh[0].text))
            # print('---')
            describe = soup_2.select('div.box-info-bd')
            describe_1 = str.convert(describe[0].text)
            # print(str.convert(describe[0].text))
            # print('---')
            daily_count = int((len(soup_2.find_all('td'))))
            print(daily_count)
            lession_json = []
            daily_a = []

            u = 45
            dt = 6
            for d in range(daily_count):
                try:
                    # print(dt)
                    url_4 = 'https:'+soup_2.find_all('a')[u]['href']
                    res_4 = requests.get(url_4, headers=headers)
                    soup_4 = BeautifulSoup(res_4.text, 'html.parser')
                    # url_3 = 'https://www.hiyd.com/bb/438_%s/'%(i+1)
                    print(url_4)
                    a = urlparse(url_4)
                    if 'dongzuo' in a[2]:
                        print('out')
                        continue
                    daily_title_4 = soup_4.find_all('span')
                    # daily_title_1 = '第 %s 天:'%(d+1) + str.convert(daily_title[d].text)
                    # daily_title_3_1 = '第 %s 天:' % (d + 1) + str.convert(daily_title_3[dt].text)
                    daily_title_4_1 = str.convert(daily_title_4[3].text) + ':'+ str.convert(daily_title_4[4].text)
                    print(daily_title_4_1)
                    print('------項目數------')
                    print(len(soup_4.select('div.action-list-wrap')))
                    item = int(len(soup_4.select('div.action-list-wrap')))

                    item_list = []
                except requests.exceptions.InvalidURL:
                    print('off day')
                    u += 1
                    dt += 1
                    continue

                    item_list = []
                try:
                    for i in range(item):
                        # print(item)
                        daily_url = soup_2.select('a.row-item')
                        # url_4 = 'https:'+soup_2.find_all('a')[u]['href']
                        # url_3 = 'https://www.hiyd.com/bb/438_%s/'%(i)
                        # u += 1
                        # res_4 = requests.get(url_4, headers=headers)
                        # soup_4 = BeautifulSoup(res_4.text, 'html.parser')
                        # print(soup_3.select('div.cont-wrap')[i].text)
                        item_1 = str.convert(soup_4.select('div.action-list-wrap')[i].text)
                        item_list.append(item_1)
                    u += 1
                    dt += 1

                except IndexError:
                        pass
                value_item = {daily_title_4_1: item_list}
                daily_a.append(value_item)

                sleeptime_1 = random.randint(7,13)
                time.sleep(sleeptime_1)
                print('睡 %s 秒' % (sleeptime_1))


            value = {'url': title_url, 'title': title_name_1, 'lesson': daily_a, 'lesson_time': times,
                     'strengh': strengh[1], 'describe': describe_1, 'time': 0, 'author': 0}

            lession_json.append(value)

            with open('./hiyd/hiyd_txt/%s.txt' % (title_name_1), 'w', encoding='utf-8-sig') as f:  #.replace('/','_')
                f.write(title_name)
                f.write('\n')
                f.write(title_url)
                f.write('\n')
                f.write(time_strengh_1)
                f.write('\n')
                f.write(describe_1)
            transform_json_string = json.dumps(lession_json, ensure_ascii=False)
                # ensure_ascii=False (要加這個文字才不會變成數字)
            with open('./hiyd/hiyd_json/%s.json' % (title_name_1).replace('/','_'), 'w', encoding='utf-8') as j:
                j.write(transform_json_string)

        sleeptime=random.randint(5, 10)
        time.sleep(sleeptime)
        print('睡 %s 秒'%(sleeptime))
        pages += 1
        print(pages)
if __name__ ==  '__main__':
    result = getArticle(15) ##需要修改


end = time.time()
print('執行時間:%f 秒'%(end - start))