from bs4 import BeautifulSoup
import requests
import time

class MyClass:

    def __init__ (self, patches):
        self.version_patches = patches


    def __get_html (self,version):

        url = f"https://liquipedia.net/dota2/Version_{version}"
        resp = requests.get(url)
        html_content = resp.content
        return url,BeautifulSoup(html_content,'html.parser')


    def check_patch(self):
        for version in self.version_patches:

            url, soup = self.__get_html(version)
            p_tag = soup.find('p')

            if p_tag:
                p_text = p_tag.text.strip()

                if "There is currently no" in p_text:
                    print (f"ERROR: {url}",False)
                else:
                    print (f"SUCCESS: {url}",True)
            else:
                print("CRITICAL ERROR: Tag specifier <p> has not been detected by bs4. The website structure might have been changed. Please recheck the HTML structure!")
       

    def __extract_data (self,version,patch_classes):

        patch_information=[]

        ctr_entity = 0
        ctr_phrases = 0

        _,soup = self.__get_html(version)
        all_h3 = soup.find_all('h3')


        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):

                ctr_entity+=ctr_entity

                patch_information.append(h3.text.strip())
                ul_container = h3.find_next('ul')
                all_li = ul_container.find_all('li')

                for i,li in enumerate(all_li):
            
                    in_line = li.find('b')

                    if (in_line):
                        patch_information.append(in_line.text.strip())
                
                    else:
                        patch_class = li.find('img',alt=lambda value: value in patch_classes)
                        if (patch_class):
                            patch_information.append(patch_class.get('alt') + " " + li.text.strip())

                            ctr_phrases+=ctr_phrases
            


        return ctr_entity,ctr_phrases,patch_information
    

    def build_data (self,patch_classes,verbose=0):
        patch_classes = patch_classes
        ctr_en=0
        ctr_en=0

        start_time = time.time()
        for version in self.version_patches:

            
            ctr_entity,ctr_phrases,patch_information = self.__extract_data(version,patch_classes)       
            ctr_en+= ctr_entity
            ctr_ph+=ctr_phrases

            with open(f"text/{version}.txt",'a') as f:
                for word in patch_information:
                    f.write(word+"\n")

            end_time = time.time()

            if verbose != 0:
                
                if verbose == 2:
                    for words in patch_information:
                        print(words+"\n")
                elif verbose == 1:
                    run_time = end_time - start_time
                    print("------------------------------")
                    print(f"Version: {self.version_patches}\n")
                    print(f"Entities: {ctr_entity}\n")
                    print(f"Phrases: {ctr_phrases}\n")
                    print(f"Parse Time: {run_time}\n")
                    print("------------------------------")
          

            


        


