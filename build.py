from bs4 import BeautifulSoup
import json
import preprocess
import requests
from pyppeteer import launch
import time




lss=[]

hero = " "
name = " "
note = " "
p_class = " "



def getPatch():

    global hero,name,note

    patch_classes = ['Buff','Rework','Nerf','Rescale','Removed','New']
    sentinel = 0

    url = f"https://liquipedia.net/dota2/Version_7.35"
    resp = requests.get(url)
    html_content = resp.content

    soup = BeautifulSoup(html_content,'html.parser')
    all_h3 = soup.find_all('h3')

    
    
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

        # if (sentinel==1):
        #     print("WALANG B AT WALANG PATCH CLASS!")
        #     sentinel=0
        # else:
        print(h3.text.strip())
        for values in lss:
            print(values)

        print("\n")
        lss.clear()

    #


         

    # STRUCTURE OF HEROES, SKILL NAME, AND ADJUSTMENTS MADE
    # <h3> - Hero name 
    # <ul> - patch container
    #   <li>
    #       <img alt=""> -> in-line note, can print the whole list immediately 
    #   <li>
    #       <b> - Skill name, must be followed up by <ul> below
    #       <ul> 
    #           <li>
    #               <img alt = ""> -> in-line note again, can print the whole list immediately
    #   <ul>
    #       <li>
    #       <li>
    #       <li> 

    # Sibling <ul> tags should be analyzed base on its <li> childs. 
    # If a <li> child contains an <img alt = "">, the it is an in-line text, wherein the patch class
    # is placed next to the note. 
    # If a <li> child contains an <b>, then its a skill / talent / shard title, wherein the <ul> tag next to 
    # it is used as a container. All list inside that container is in-line similar to the first example.  


    # There should be a function that accepts a <li> tag and analyzed it if its an immediate in-line
    # or secondary in-line. If immediate, then return the patch_class + patch_note immediately. If not
    # then fetch the <b> tag to get the skill/shard/talent name and analyze the <ul> again. 




getPatch()