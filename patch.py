from bs4 import BeautifulSoup
import requests
from pyppeteer import launch
import asyncio
import os


# <li><img alt = "">

alt_target = ["Buff","Nerf"]

url = "https://liquipedia.net/dota2/Version_7.35"
resp = requests.get(url)
html_content = resp.content

soup = BeautifulSoup(html_content,'html.parser')

for li in soup.find_all('li'):
    #img = li.find('img')

    img_tag = li.find('img',alt=lambda value: value in alt_target)
    if(img_tag):
    
        if (li.find("span")):
            continue

        #print(img_tag.get('alt'),)
        #print("\n")

        if (img_tag.get('alt') == "Buff"):
            file_name = "buff_data.txt"

        elif (img_tag.get('alt')== "Nerf"):
            file_name = "nerf_data.txt"

        with open (f"dataset/{file_name}","a",encoding="utf-8", newline='') as f:
            f.write(li.text.strip() + "\n")

    