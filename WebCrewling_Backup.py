import requests
from bs4 import BeautifulSoup
import re

#total_url에 크롤링할 url 입력
total_url = 'https://subslikescript.com/series/Screen_One-297625'
response = requests.get(total_url)
titles = list()

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select("a")
    for href in soup.find("div", class_="series_seasons").find_all("li"):
        titles.append(href.find("a")["href"])

else:
    print(response.status_code)

for i in titles:
    url = 'https://subslikescript.com' + i

    html = requests.get(url)
    soup = BeautifulSoup(html.text)

    if html.status_code == 200:
        script_tag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])
        script_tags = ['body > div > div > main > nav.prevnext',
                       'body > div > div > main > article > h1',
                       'body > div > div > main > nav:nth-child(1) > ul',
                       'head > title']

        for script in script_tag:
            script.extract()

        for i in script_tags:
            script_tag2= soup.select_one(i)
            script_tag2.extract()

        content = soup.get_text('\n', strip=True)
        #print(content)

        f1=open('crawling.txt','w',encoding='UTF-8')
        f1.write(content)
        f1.close()

        # 스크립트 파일 정제
        f2=open('crawling.txt','r',encoding='UTF-8') # 정제되기 전의 파일
        f3=open('crawling_raw.txt','w',encoding='UTF-8')# 정제된 후의 파일
        for line in f2:
            f3.write(line.replace('?','.'))

        f2.close()
        f3.close()



    else:
        print(html.status_code)

