from bs4 import BeautifulSoup
import preprocess
import requests
from pyppeteer import launch




def dataset():

    ctr = 0
    patch_versions = ["7.35","7.34","7.33","7.32","7.31"]
    alt_texts = ["Buff","Nerf","Rework"]

    for version in patch_versions:
 
        if ctr < 2:
            data_path = "dataset/train"
        else:
            data_path = "dataset/test"

        ctr+=1

        url = f"https://liquipedia.net/dota2/Version_{version}"
        resp = requests.get(url)
        html_content = resp.content

        soup = BeautifulSoup(html_content,'html.parser')

        for li in soup.find_all('li'):

            if (li.find("span")):
                continue

            img_tag = li.find('img',alt=lambda value: value in alt_texts)

            if(img_tag):
                
                alt = img_tag.get('alt')
            
                with open (f"{data_path}/{alt}.txt","a",encoding="utf-8", newline='') as f:
                    raw_text = li.text.strip()
                    clean = preprocess.purge(raw_text)
                    f.write(clean+"\n")
        
