import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

class CrawlerUtility:
    @classmethod
    def oneindiascrape(self, start, end):
        news_data = []
        label_data = []

        for i in range(start, end+1):
            print("Accessing page - ",i)
            URL = "https://malayalam.oneindia.com/fact-check/?page-no="+str(i)
            webpage = requests.get(URL, allow_redirects=False)
            if(webpage.is_redirect):
                break
            soup = BeautifulSoup(webpage.text, 'html.parser')
            table = soup.find_all('div',attrs={'class':'cityblock-title news-desc'})
            for link in table:
                try:
                    parsed = link.find('a', href = True)
                    URL = 'https://malayalam.oneindia.com'+str(parsed['href'])
                    webpage = requests.get(URL)
                    soup = BeautifulSoup(webpage.text,'html.parser')
                    title = soup.find('h1', attrs={'class':'heading'})
                    title = title.text
                    table = soup.find_all('div', attrs={'class':'oi-factcheck-block'})
                    news = table[0].find('p')
                    news = news.text
                    rating = table[2].find('div')
                    rating = rating.text
                    statement_news = title+". "+news
                    news_data.append(statement_news)
                    label_data.append(rating)
                except Exception:
                    continue
        return news_data, label_data

    @classmethod
    def samayamscrape(self, start, end):
        false_news = []
        itr = start
        for page in range(start, end):
            print('Accessing page - ',itr)
            itr+=1
            URL = 'https://malayalam.samayam.com/latest-news/fact-check/articlelist/66765139.cms?curpg='+str(page)
            webpage = requests.get(URL, allow_redirects=False)
            if(webpage.is_redirect):
                break
            soup = BeautifulSoup(webpage.text, 'html.parser')
            table = soup.find_all('a', attrs={'class':'table_row'})
            if len(table) == 0:
                break
            for i in table:
                URL = i['href']
                webpage = requests.get(URL)
                soup = BeautifulSoup(webpage.text, 'html.parser')
                news = soup.find('title')
                news = news.text
                output = re.sub(r'\s*[A-Za-z]+\b', '' , news)
                output = output.rstrip()
                output = output.split(' ')
                for i in output:
                    if i=='|':
                        output.remove(i)
                    elif i=='-':
                        output.remove(i)
                    elif i==':':
                        output.remove(i)
                    elif i=='::':
                        output.remove(i)
                a = ' '.join(output)
                false_news.append(a)
        return false_news, ['False' for i in range(len(false_news))]

    @classmethod
    def news18scrape(self, start, end):
        l = []
        for page in range(start, end):
            print('Accessing page ',page)
            URL = 'https://malayalam.news18.com/india/page-'+str(page)+'/'
            webpage = requests.get(URL)
            soup = BeautifulSoup(webpage.text, 'html.parser')
            table = soup.find_all('div',class_="blog-list-blog")
            for i in table:
                text = i.find('img')
                text = text['title']
                text = re.sub(r'\s*[A-Za-z]+\b', '' , text)
                text = text.rstrip()
                output = text.split(' ')
                for i in output:
                    if i=='|':
                        output.remove(i)
                    elif i=='-':
                        output.remove(i)
                    elif i==':':
                        output.remove(i)
                    elif i=='::':
                        output.remove(i)
                a = ' '.join(output)
                l.append(a)
        return l, ['True' for i in range(len(l))]