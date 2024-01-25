from bs4 import BeautifulSoup
import requests
import time
import os 

class DatasetBuilder:

    target_classes = ['Buff',"Nerf","New","Rework","Rescale","Removed"]

    def __init__ (self, patch):
        self.version_patch = patch

    def __check_eol(self,patch_stage):
        for i,contents in enumerate(patch_stage):
            if (("[edit]" in contents) and (patch_stage[i+1] == " ")):
                    return True

    def get_html (self):

        url = f"https://liquipedia.net/dota2/Version_{self.version_patch}"
        resp = requests.get(url)
        html_content = resp.content
        return BeautifulSoup(html_content,'html.parser')
    
    def get_patch (self):

        patch_stage=[]
        patch_final=[]
      
        soup = self.get_html()
        hero_start = soup.find('span',id='Heroes')
        all_h3 = hero_start.find_all_next('h3')
 
        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):


                patch_stage.append(h3.text.strip())

                ul_container = h3.find_next('ul')
                all_li = ul_container.find_all('li')

                for i,li in enumerate(all_li):
             
                    in_line = li.find('b')

                    if (in_line):

                        if (in_line.text.strip() == "Talent"):
                            title = "[talent]"
                        else:
                            title = "[skill]"

                        patch_stage.append(in_line.text.strip() + f"{title}")
                
                    else:
                        patch_class = li.find('img',alt=lambda value: value in self.target_classes)
                        if (patch_class):
                            patch_stage.append(patch_class.get('alt') + " " + li.text.strip())

         
                patch_stage.append(" ")
            
                if (not(self.__check_eol(patch_stage))):
                    patch_final += patch_stage
                else:
                    continue

                patch_stage.clear()

        return patch_final
    
    

        
    # def get_html(self,version,beautify=True):
    #     return self.__parse_html(version).prettify()

                    
    # def build_data (self,save=False):
    #     start_time = time.time()
    #     for version in self.version_patch:
    #         patch_information = self.__extract_data(version)       
       
    #         if save:
                



     
 
          

    
patches = ["7.31","7.32","7.33","7.34","7.35"]


for patch in patches:
    obj = DatasetBuilder(patch)
    patch_list = obj.get_patch()

    with open(f"text/{patch}.txt",'w') as f:
        for word in patch_list:
            f.write(word+"\n")

 
