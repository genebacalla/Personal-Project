from bs4 import BeautifulSoup
import preprocess
import requests
from pyppeteer import launch




def dataset():

    ctr = 0
    patch_versions = ["7.30c","7.30d","7.30e","7.31","7.31b","7.31c","7.31d","7.32","7.32b","7.32c","7.32d","7.32e","7.33","7.33b","7.33c","7.33d","7.34","7.34b","7.34c","7.34d","7.34e","7.35"]
    alt_texts = ["Buff","Nerf","Rework"]

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

    # Extact all <h3> in the HTML page which contains the item or hero name
    for h3_tag in soup.find_all('h3'):

        # Check if a ul tag is present right next to h3, indicating that it is a valid patch container
        ul_tag = h3_tag.find_next_sibling('ul')
        
    
        if (ul_tag):
            
            # If valid patch container, extract all list tags inside that container
            ul_soup = ul_tag.find_all('li')

            if (ul_soup):
                print(h3_tag.text.strip())

                # Iterate over all detected list tags inside that patch container
                for list_tag in ul_soup:

                    # If the immediate tag is span, ignore iteration since its the skill name. Including the skill name is planned for future development.  
                    if (list_tag.find('span')):
                        continue

                    print(list_tag.text.strip())
                #     print(patch_notes.text)
            
        print("\n")
            # entity_name = h3_tag.text

            # print(h3_tag.text)
            # # print(ul_tag.text)
            # print("\n")



        # img_tag = li.find('img',alt=lambda value: value in alt_texts)

        # if(img_tag):
            
        #     alt = img_tag.get('alt')
        
        #     # with open (f"{data_path}/{alt}.txt","a",encoding="utf-8", newline='') as f:
        #     #     raw_text = li.text.strip()
        #     #     clean = preprocess.purge(raw_text)
        #     #     f.write(clean+"\n")
        

dataset()