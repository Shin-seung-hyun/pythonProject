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
        r = open('crawling.txt', 'r+', encoding='UTF-8')
        w = open('crawling_raw.txt', 'a+', encoding='UTF-8')

        while True:
            line = r.readline()
            if not line: break

            # if '"' in line:  # '"' 제거
            #     line = line.replace('"', '')

            # if '#' in line:  # '#' 제거
            #     line = line.replace('#', '')

            # if '- ' in line:  # '- ' 제거
            #     line = line.replace('- ', '')

            if '!' in line:  # '!' -> '.'
                line = line.replace('!', '.')

            if '&' in line:  # '&' -> 'and'
                line = line.replace('&', 'and')

            if 'um...' in line:  #소문자 'um...' -> 'um.'
                line = line.replace('um...', 'um.')

            if 'Um...' in line:  #대문자'Um...' -> 'Um.'
                line = line.replace('Um...', 'Um.')

            if 'Mmm-mmm...' in line:  # 'Mmm-mmm...' -> 'Mmm mmm.'
                line = line.replace('Mmm-mmm...', 'Mmm mmm.')

            if 'so...' in line:  # 'so...' -> 'so.'
                line = line.replace('um...', 'um.')

            if 'uh...' in line:  # 'uh...' -> 'uh.'
                line = line.replace('um...', 'um.')

            if 'a.m.' in line:  # 'a.m.' -> 'am'
                line = line.replace('a.m.', 'am')

            if 'p.m.' in line:  # 'p.m.' -> 'pm'
                line = line.replace('p.m.', 'pm')

            if 'e-mail' in line:  # 'e-mail' -> 'email'
                line = line.replace('e-mail', 'email')

            if 'T-shirt' in line:  # 'T-shirt' -> 'Tshirt'
                line = line.replace('T-shirt', 'Tshirt')

            # matchObj=re.search('\([A-Z].*\)\s',line) #(문장)제거
            # if (matchObj != None):
            #     line = re.sub(pattern='\([A-Z].*\)\s',repl='', string=line)

            w.write(line)

        r.close()
        w.close()

    else:
        print(html.status_code)

    line = re.sub(pattern='\([A-Z].*\)\s', repl='', string=line)
    line = re.sub(pattern='\[[A-Z].*\]\s', repl='', string=line)
    line = re.sub(pattern='^♪\s[A-Z].*', repl='', string=line)
    line = re.sub(pattern='^\s', repl='', string=line)  # 항상 맨 마지막에 있어야하는 공백 제거

    rm_pattern = [
        '\([A-Z].*\)\s',  # [문장] 제거
        '\[[A-Z].*\]\s',  # (문장) 제거
        '^♪\s[A-Z].*',  # '♪' 문장 제거
        '\-\s'   # '-' 제거
        '\#'    # '#' 제거
        '"'     # " 제거
        "^(')"  # '문장' '의 제거
        "\s(')$"
        '[A-Z].*\:\s' # '이름:' 제거

        '^\s'  #공백제거 (제일 나중에 해야함)
    ]

    for i in rm_pattern:
        line = re.sub(pattern=rm_pattern, repl='', string=line)
        w.write(line)
