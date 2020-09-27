# dcard_weightloss  抓取json ,txt已關閉

import requests
from bs4 import BeautifulSoup
import os
import json
import time
import random
import pymongo
import re
###
client = pymongo.MongoClient('192.168.158.128', 27017)
db = client.tibame
collection = db.dcard_weightloss
###
try:
    with open('./dcard_weightloss/url_list.txt', 'a+', encoding='utf-8') as file:
        file.close()
except:
    pass
# 建立目標目錄及資料夾
# resource_path = r'./dcard_weightloss'
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./dcard_weightloss/json' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
# resource_path = r'./dcard_weightloss/txt' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)
start = time.time()
# 目標網址
url = 'https://www.dcard.tw/service/api/v2/forums/weight_loss/posts?limit=100&before=%s'
headers = {}
ua ='''#authority: www.dcard.tw
# method: GET
# path: /service/api/v2/forums/fitness/posts?popular=true&limit=100&before=234245580
# scheme: https
# accept: */*
# accept-encoding: gzip, deflate, br
# accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
# cookie: __auc=c44b29b917226b659aea129389c; _gid=GA1.2.950276719.1597821560; G_ENABLED_IDPS=google; dcsrd=Ds4SLhwp0-K1nqPorYkjk3Rh; dcsrd.sig=XPyF8lpdTQtph6VaIACzG3XO6TA; dcard=eyJ0b2tlbiI6ImV5SmhiR2NpT2lKRlpFUlRRU0lzSW10cFpDSTZJbEpMTFVoZlRUUm9VVkpET1dzeFUxcEdZMEZ1UkRBMVZreFljV1JZUm1kUVZYQXdWbGx0YjJ4eWFqZzlJbjAuZXlKaGNIQWlPaUpqTW1VM05qTTVOUzB6T0dFeExUUTRaamN0WVRsbE1DMWhaamN6TldJNFpqZGpOREVpTENKbGVIQWlPakUxT1RjNE9UZzJNek1zSW1saGRDSTZNVFU1TnpnNU9ETXpNeXdpYVhOeklqb2laR05oY21RaUxDSnFkR2tpT2lJMllUTXhNbUV5WVMweFpEVmlMVFEyWWpJdFlqWXlaQzB4Wm1aaE4yVTVNall6TW1FaUxDSnpZMjl3WlhNaU9sc2liV1Z0WW1WeUlpd2liV1Z0WW1WeU9uZHlhWFJsSWl3aVpXMWhhV3dpTENKbGJXRnBiRHAzY21sMFpTSXNJbVJsZG1salpTSXNJbVJsZG1salpUcDNjbWwwWlNJc0luQm9iM1J2SWl3aWJtOTBhV1pwWTJGMGFXOXVJaXdpWm05eWRXMDZjM1ZpYzJOeWFXSmxJaXdpY0c5emRDSXNJbkJ2YzNRNmMzVmljMk55YVdKbElpd2labUZqWldKdmIyc2lMQ0pqYjJ4c1pXTjBhVzl1SWl3aVkyOXNiR1ZqZEdsdmJqcDNjbWwwWlNJc0lteHBhMlVpTENKd2IzTjBPbmR5YVhSbElpd2lZMjl0YldWdWREcDNjbWwwWlNJc0luSmxjRzl5ZENJc0ltWnlhV1Z1WkNJc0ltWnlhV1Z1WkRwM2NtbDBaU0lzSW0xbGMzTmhaMlVpTENKdFpYTnpZV2RsT25keWFYUmxJaXdpY0dodmJtVWlMQ0p3YUc5dVpUcDJZV3hwWkdGMFpTSXNJbkJvYjI1bE9uZHlhWFJsSWl3aWNHVnljMjl1WVNJc0ltTnZibVpwWnlJc0ltTnZibVpwWnpwM2NtbDBaU0lzSW5SdmEyVnVPbkpsZG05clpTSXNJbkJsY25OdmJtRTZkM0pwZEdVaUxDSndaWEp6YjI1aE9uTjFZbk5qY21saVpTSXNJbVp2Y25WdElpd2liV0YwWTJnaUxDSnRZWFJqYURwM2NtbDBaU0lzSW5SdmNHbGpJaXdpZEc5d2FXTTZjM1ZpYzJOeWFXSmxJaXdpWm1WbFpEcHpkV0p6WTNKcFltVWlMQ0p5WldGamRHbHZiaUlzSW5KbFlXTjBhVzl1SWl3aWNtVmhZM1JwYjI0aUxDSnlaV0ZqZEdsdmJpSXNJbXh2WjJsdVZtVnlhV1pwWTJGMGFXOXVJaXdpYkc5bmFXNVdaWEpwWm1sallYUnBiMjQ2ZG1WeWFXWjVJbDBzSW5OMVlpSTZJakU0TURBek1TSjkuU2pIaVhMUFRUSFJEcUJQNm1IRnF4RWxjakhFbzR3NEdwWjhLdnZ3QnkwZFFJT2gzSTlMM1cydEVaZ2V6aUJvSng1OUpOMzFad1lKeHJRSmNmNHhpQkEiLCJ0b2tlbkV4cGlyeSI6MTU5Nzg5ODYzMzY2MiwicmVmcmVzaFRva2VuIjoiSlQra3I1VFZRMGF3MW05MmNIR2hIZz09IiwiX2V4cGlyZSI6MTYwMDQ5MDMzMzY2MiwiX21heEFnZSI6MjU5MjAwMDAwMH0=; dcard.sig=L9DUNk-J6AAXzHsQmGYNbOE7uo4; __asc=a949af6a1740a29a7186c4f1f92; _gat=1; _ga=GA1.1.465292436.1588179391; __cfduid=df6d530a99804697ee192b8c85546a0b61597898405; _ga_C3J49QFLW7=GS1.1.1597898335.17.1.1597898431.0
# if-none-match: W/"87b-zrSBwbRZH+yJrrRPYHWjowHH0JI"
# referer: https://www.dcard.tw/f/weight_loss
# sec-fetch-dest: empty
# sec-fetch-mode: cors
# sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]]=i.split(": ")[1]
    # print(i)

def savemongodb(value):
    insert_item = value
    insert_result = db.dcard_weightloss.insert_one(insert_item)
    print(insert_result)

# 利用dcard jsonid 抓取文章資訊
def getArticle(before):
    # before = 234271171

    try:
        # 抓取每個 json 檔 持續 100次
        for times in range(100):
            res = requests.get(url%(before), headers=headers)
            # print(res)
            soup = BeautifulSoup(res.text,'html.parser')
            # print(soup)
            content_json = json.loads(soup.text)
            # print(content_json)
            url2 = 'https://www.dcard.tw/f/weight_loss/p/%s'

            # 抓取每篇json 檔 100筆 內容
            for i in range(100):

                weight_loss_json = []
                content_id = (content_json[i]['id'])
                print(content_id)
                res_2 = requests.get(url2%(content_id), headers=headers)
                # print(res_2)
                soup_2 = BeautifulSoup(res_2.text,'html.parser')
                # print(soup_2.text)
                content_title = soup_2.select("div>div>div>div>div>div>div>article>div>div>h1")
                # print(content_title[0].text)
                # 判斷是否已抓取過
                # filepath = './dcard_weightloss/json/%s.json' % (content_id)
                # if os.path.isfile(filepath):
                #     print("gotcha")
                #     continue
                # else:
                #     print("New for start")
                try:
                    content_time = soup_2.select("div>div>div>div>div>div>div>article>div>div")
                    a = content_time[2].text
                    # print(content_time[2].text)
                except:
                    content_time = '無'
                    a = content_time
                    # print(content_time)
                try:
                    content_content = soup_2.select("div>div>div>div>div>div>div>article>div>div>div")
                    b = content_content[0].text
                    # print(content_content[0].text)
                except IndexError:
                    content_content = '無'
                    b = content_content
                    # print(content_content)
                try:
                    content_tag = soup_2.select("div>div>div>div>div>div>div>article>div>ul")
                    c = content_tag[0].text
                    # print(content_tag[0].text)
                except IndexError:
                    content_tag = '無'
                    c = content_tag
                    # print(content_tag)
                with open('./dcard_weightloss/url_list.txt', 'r', encoding='utf-8') as f:
                    file = f.readlines()
                    url_list = []
                    for i in file:
                        result = i.replace('\n', '')
                        url_list.append(result)
                    if url2%(content_id) in url_list:
                        print('gotcca')
                        continue
                    else:
                        print('new')
                        value = {}
                        value['url'] = url2%(content_id)
                        value['title'] = content_title[0].text
                        value['lesson'] = 0
                        value['lesson_time'] = 0
                        value['strengh'] = 0
                        value['describe'] = b
                        value['time'] = a
                        value['author'] = 0
                        savemongodb(value)

                        with open ('./dcard_weightloss/url_list.txt','a',encoding='utf-8') as u:
                            out_str = url2%(content_id) + '\n'
                            u.write(out_str)

                # with open ("./dcard_weightloss/txt/%s.txt"%(content_id),'w',encoding='utf-8') as f:
                #
                #     f.write(content_title[0].text)
                #     f.write('\n')
                #     f.write(a)
                #     f.write('\n')
                #     f.write(b)
                #     f.write('\n')
                #     f.write(c)
                #     f.write('\n')
                #     f.write(url2 % (content_id))
                # fitness_json_string = json.dumps(weight_loss_json, ensure_ascii=False)
                # # ensure_ascii=False (要加這個文字才不會變成數字)
                # with open('./dcard_weightloss/json/%s.json'%(content_id), 'w', encoding='utf-8') as f:
                #     f.write(fitness_json_string)

            # print(content_json[-1]['id'])
            last_content_id = (content_json[-1]['id'])
            # print(last_content_id)
            # 利用json檔最後一筆id當作新的'json開頭ID',帶回before
            before = last_content_id
            # print(last_article_id)

            sleeptime=random.randint(3, 5)
            time.sleep(sleeptime)
    # except IndexError:
    #         pass

    except IndexError:
            pass
if __name__ ==  '__main__':
    # 先至該看板 按下f12 找到 json ID 填入
    result = getArticle(233961259) ##需要修改
end = time.time()
print('執行時間:%f 秒'%(end - start))
print('finish')