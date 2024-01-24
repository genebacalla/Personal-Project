from bs4 import BeautifulSoup
import json
import preprocess
import requests
from pyppeteer import launch
import time
import sys




lss=[]



def getPatch():


    patch_classes = ['Buff','Rework','Nerf','Rescale','Removed','New']
    sentinel = 0

    url = f"https://liquipedia.net/dota2/Version_7.35"
    resp = requests.get(url)
    html_content = resp.content


    soup = BeautifulSoup(html_content,'html.parser')
   
    p = soup.find('p')
    all_h3 = soup.find_all('h3')

    print(all_h3)
    
    time.sleep(10)
    
    for i,h3 in enumerate(all_h3):
        
    
        if (h3.find_next('ul')):
            
            #print(h3.text.strip())
            ul_container = h3.find_next('ul')


            all_li = ul_container.find_all('li')

            for i,li in enumerate(all_li):
                    
                in_line = li.find('b')

                if (in_line):
                    #print(in_line.text.strip())
                    lss.append(in_line.text.strip())
               
                else:
                    patch_class = li.find('img',alt=lambda value: value in patch_classes)
                    if (patch_class):
                        #print(patch_class.get('alt') + " " + li.text.strip())
                        lss.append(patch_class.get('alt') + " " + li.text.strip())
          
                    else:
                        sentinel=1

        print(h3.text.strip())
        for values in lss:
            print(values)

        print("\n")
        lss.clear()



getPatch()