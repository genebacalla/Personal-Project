from bs4 import BeautifulSoup
import json
import preprocess
import requests
from pyppeteer import launch



hero_name = ""
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
            ul_soup1 = ul_tag1.find_all('li')

            if ul_soup1:

                for li_tag1 in ul_soup1:
                    
                    ul_soup2 = li_tag1.find("ul")
                    
                    if (ul_soup2):

                        li_soup = li_tag1.find_all('li')
                        for li_tag2 in li_soup:
                            imgAlt_tag = li_tag2.find('img',alt=lambda value: value in alt_texts)

                            if imgAlt_tag:
                                print(imgAlt_tag.get('alt')+" "+li_tag2.text.strip())

                    else:
                        imgAlt_tag = li_tag1.find('img',alt=lambda value: value in alt_texts)
                        if imgAlt_tag:
                            print(imgAlt_tag.get('alt')+" "+li_tag1.text.strip())

              

                    # entity_name = li_tag1.find('b')
                    # li_soup = li_tag1.find_all('li')
                    # if (entity_name):
                    #     hero_name = h3_tag.text.strip()

                    #     print(h3_tag.text.strip())
                    #     print(entity_name.text.strip())

                    # print("tag1: "+li_tag1.text)
          
               
                    
                    # for li_tag2 in li_soup:
                    #     print(li_tag2.text.strip())
                        # entity_class = li_tag2.find('img',alt=lambda value: value in alt_texts)
                        # entity_patch = li_tag2.text.strip()
                        
             
            
                        # if entity_class:
                        #     print(entity_class.get('alt'),entity_patch)
                        # else:
                        #     print("HOLDER")
               
                    

                    
        print("\n")

                    # # extract all span tags inside <li> container
                    # for span_tag in li_soup_forSpan:

                    #     skill_name = span_tag.find("b")


                    #     if (skill_name):
                    #         if (skill_name.text.strip() != "Talent"):
                    #             print(skill_name.text.strip())

                    #     for ul_tag in li_soup_forUl:

                    #         ul_soup_forUL = ul_tag.find_all('li')

                    #         for patch_note in ul_soup_forUL:

                    #             patch_description = patch_note.find('img',alt=lambda value: value in alt_texts)
                    #             if (patch_description):
                    #                 print(patch_description.get('alt')+" " +patch_note.text.strip())
                          
            
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