from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
from pyppeteer import launch

class BuildDataset:

    def __init__(self,patch_version):
        self.patch_version = patch_version


    def purge(self,text):
        tokens = word_tokenize(text)

        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.isalpha() and word.lower() not in stop_words]
        
        purged_text = ' '.join(tokens)
        return purged_text

    def build_data(self,patch_type):

        valid_patch_type = ["Buff","Nerf","Rework"]

        patch_type = patch_type.strip().capitalize()

        if not (patch_type in valid_patch_type):
            print("Invalid patch type!")
            return
        else:
            url = f"https://liquipedia.net/dota2/Version_{self.patch_version}"
            resp = requests.get(url)
            html_content = resp.content

            soup = BeautifulSoup(html_content,'html.parser')

            for li in soup.find_all('li'):
                if (li.find("span")):
                    continue

                img_tag = li.find('img',alt=patch_type)

                if(img_tag):
                    with open (f"dataset/{patch_type}.txt","a",encoding="utf-8", newline='') as f:
                        raw_text = li.text.strip()
                        clean = self.purge(raw_text)
                        f.write(clean + "\n")
             

