# ptt fitness  抓取json ,txt已關閉
import requests
from bs4 import BeautifulSoup
import os
import json
import time

# 建立目標目錄及資料夾
resource_path = r'./ptt_fitness'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
resource_path = r'./ptt_fitness/json' ##需要修改
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
# resource_path = r'./ptt_fitness/txt' ##需要修改
# if not os.path.exists(resource_path):
#     os.mkdir(resource_path)

start = time.time()
#目標網址
url = 'https://www.ptt.cc/bbs/FITNESS/index%s.html'
headers = {}
ua ='''authority: www.ptt.cc
# method: GET
# path: /bbs/FITNESS/M.1597028756.A.B6B.html
# scheme: https
# accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# accept-encoding: gzip, deflate, br
# accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
# cache-control: max-age=0
# cookie: _ga=GA1.2.928340325.1584630566; __cfduid=d73baffdcee13e9e47ac842d6f9d5e37b1596700384; __cf_bm=4538da972af3ed5bf6aa2201701e4d5ad4ca1ee1-1597587091-1800-ARM3BEwGHOdhx/S9sUAXj1UV2YKp/Avg5FCKzOCWuHOyQgQZ4TuUaxU5VrB41TmzGcAjKcJKxTXRHYnizGm1pU0=; _gid=GA1.2.595792866.1597587091; _gat=1
# sec-fetch-dest: document
# sec-fetch-mode: navigate
# sec-fetch-site: none
# sec-fetch-user: ?1
# upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'''
for i in ua.split("\n"):
    headers[i.split(": ")[0]]=i.split(": ")[1]
    # print(i)
def getArticle(page):
    # 起始頁為 1
    pages = 1
    fitness_json = []
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
                # 判斷是否已抓取過
                filepath = './ptt_fitness/json/%s.json' % (title_name)
                if os.path.isfile(filepath):
                    print("gotcha")
                    continue
                else:
                    print("New for start")
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
                fitness_json_dict = {}
                value = {'url': url_2, 'title': title_name, 'lesson': 0, 'lesson_time': 0,
                          'strengh': 0, 'describe': article[0].text.split('--')[0], 'time': article_time[2].text, 'author': 0}
                fitness_json.append(value)
                # with open ("./ptt_fitness/txt/%s.txt"%(title_name),'w',encoding='utf-8') as f:
                #     f.write(title_name)
                #     f.write('\n')
                #     f.write(article_time[2].text)
                #     f.write('\n')
                #     f.write(article[0].text.split('--')[0])
                #     f.write('\n')
                #     f.write(url_2)
                fitness_json_string = json.dumps(fitness_json, ensure_ascii=False)
                # ensure_ascii=False (要加這個文字才不會變成數字)
                with open('./ptt_fitness/json/%s.json"%(title_name)', 'a', encoding='utf-8') as f:
                    f.write(fitness_json_string)
                # article_s = article.split('--')
                # with open('ptt_fitness.csv', 'a', newline='') as csvFile:
                #     writer = csv.writer(csvFile)
                #     writer.writerow([title_name, article_all])
                #print(article_s[0])
                # print('---------')
            except:
                pass


        pages += 1
        time.sleep(5)

if __name__ ==  '__main__':
    # 填入目標頁數
    result = getArticle(15) ##需要修改
end = time.time()
print('執行時間:%f 秒'%(end - start))
print('finish')