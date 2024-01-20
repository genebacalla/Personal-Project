from bs4 import BeautifulSoup
import json
import preprocess
import requests
from pyppeteer import launch



hero_name = ""
patch_category=""
patch_class=""
patch_note=""

dict_skill = {}
dict_talent = {}


def dataset():



    ctr = 0
    patch_versions = ["7.30c","7.30d","7.30e","7.31","7.31b","7.31c","7.31d","7.32","7.32b","7.32c","7.32d","7.32e","7.33","7.33b","7.33c","7.33d","7.34","7.34b","7.34c","7.34d","7.34e","7.35"]
    alt_texts = ["Buff","Nerf","Rework","New","Rescale","Removed"]

    # for version in patch_versions:

    # if ctr < round((len(patch_versions)/2)+2):
    #     data_path = "dataset/train"
    # else:
    #     data_path = "dataset/test"

    # ctr+=1

    url = f"https://liquipedia.net/dota2/Version_7.35"
    resp = requests.get(url)
    html_content = resp.content

    soup = BeautifulSoup(html_content,'html.parser')


    for h3_tag in soup.find_all('h3'):
        ul_tag1 = h3_tag.find_next_sibling('ul')
        
        if ul_tag1:
            print(h3_tag.text.strip())
            # hero_name = h3_tag.text.strip()
            # print(hero_name)
            ul_soup1 = ul_tag1.find_all('li',recursive=False)

            if ul_soup1:

                for li_tag1 in ul_soup1:
           
        
                    ul_soup2 = li_tag1.find("ul")
                    
                    if (ul_soup2):

                        li_soup = li_tag1.find_all('li')
                        category = li_tag1.find('b')

                        if category:
                            patch_category = category.text.strip()
                            print(patch_category)
    
                        
                        for li_tag2 in li_soup:
                            imgAlt_tag = li_tag2.find('img',alt=lambda value: value in alt_texts)

                            if imgAlt_tag:
                                print(imgAlt_tag.get('alt')+" "+li_tag2.text.strip())
                                # patch_class = imgAlt_tag.get('alt')
                                # patch_note = li_tag2.text.strip()
                    else:
                        imgAlt_tag = li_tag1.find('img',alt=lambda value: value in alt_texts)
                        if imgAlt_tag:
                            print(imgAlt_tag.get('alt')+" "+li_tag1.text.strip())
                            # patch_class = imgAlt_tag.get('alt')
                            # patch_note = li_tag1.text.strip()
                            
        print("\n")


  
        

dataset()