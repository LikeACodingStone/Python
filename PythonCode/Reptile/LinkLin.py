import requests
import json
import re
import csv
from time import sleep
from random import randint
from bs4 import BeautifulSoup

urlArray = []
urlFirstPage = f'https://www.linkedin.com/jobs/search/?currentJobId=3942423513&keywords=C%2B%2B&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true'
urlArray.append(urlFirstPage)
pageNum = 25
for index in range(1, 30):
    urlCurrent = urlFirstPage + "&start=" + str(index *pageNum)
    urlArray.append(urlCurrent)


def check_keyword_in_web(url, keyword):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if keyword in response.text:
                return True
            else:
                return False
    except requests.exceptions.RequestException as e:
        pass
    return False


jobArray = []
url = f'https://www.linkedin.com/jobs/search?keywords=C%2B%2B&location=%E6%9D%B1%E4%BA%AC&geoId=116533912&trk=guest_homepage-basic_jobs-search-bar_search-submit&position=1&pageNum=0'
response = requests.get(url = url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    with open("link.txt", "w", encoding='utf-8') as fp:
        fp.write(soup.text)
    # aTag = soup.find_all('a', class_='base-card__full-link') 
    # hrefLinks = []
    # for tag in aTag:
    #     hrefLinks.append(tag['href'])
    # for link in hrefLinks:
    #     if check_keyword_in_web(link, "toeic"):
    #         print("===> " + link + "\n")

