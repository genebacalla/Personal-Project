from bs4 import BeautifulSoup
import requests
from pyppeteer import launch
import asyncio
import os

url = "https://liquipedia.net/dota2/Version_7.35"
resp = requests.get(url)
html_content = resp.content

soup = BeautifulSoup(html_content,'html.parser')
with open("text/html_text.txt", "w", encoding="utf-8") as f:
    f.write(str(soup))


mark = "<div class='content-ad-block navigation-not-searchable'>"

with open("text/html_text.txt", "r", encoding="utf-8") as f:
    file_content = f.read()

start_index = file_content.find(mark)
end_index = file_content.rfind(mark)

if start_index != -1 and end_index != -1:
    cut_content = file_content[start_index + len(mark):end_index].strip()

    # Save the cut content to a new text file
    with open("text/html_text.txt", "w", encoding="utf-8") as f:
        f.write(cut_content)

