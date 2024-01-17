from bs4 import BeautifulSoup
import requests
from pyppeteer import launch
import asyncio
import os


# <li><img alt = "">

data_list = []

url = "https://liquipedia.net/dota2/Version_7.35"
resp = requests.get(url)
html_content = resp.content

soup = BeautifulSoup(html_content,'html.parser')

for li in soup.find_all('li'):
    #img = li.find('img')

    if(li.find('img',alt='Buff') or li.find('img',alt='Nerf')):
        img = li.find('img',alt='Buff')
        #a_tag = li.find("a")

        if (img):
            print(img)
            print(li.text)
            print("\n")

    