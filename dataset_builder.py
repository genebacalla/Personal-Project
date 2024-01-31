from bs4 import BeautifulSoup
import requests
import time
import json
import os 

class DatasetBuilder:

    _target_classes = ['Buff',"Nerf","New","Rework","Rescale","Removed","Rework"]
    _h2_hero_id = ['Heroes','Hero_Updates']
    _target_titles = ['Name','Talent','Skill']
    

    def __init__ (self, patch):
        self.version_patch = patch

    def __check_eol(self,patch_stage):
        for i,contents in enumerate(patch_stage):
            if (("[edit]" in contents) and (patch_stage[i+1] == " ")):
                    return True
            
    def __flush_compile_vars():
        _dict1={}
        _dict2={}
        _flag1=False
        _flag2=False
        str1=''
        str2=''
        return _dict1,_dict2,_flag1,_flag2,str1,str2

    def get_html (self):

        url = f"https://liquipedia.net/dota2/Version_{self.version_patch}"
        resp = requests.get(url)
        html_content = resp.content
        return BeautifulSoup(html_content,'html.parser')
    




    def mekus (self,words):

        d_lab={'Buff':0,'Nerf':0,'New':0,'Rework':0,'Rescale':0,'Removed':0}
     
        dict_main={}
        dict_stage={}
        is_end=False
        is_attribute=False
        this_key,this_value='',''

        for i,word in enumerate(words):
            if (word == " "):
                continue

            _curr_phrase=word.split(',')
            curr_key,curr_value=_curr_phrase[0],_curr_phrase[1]
            next_key= words[i+1].split(',')[0]

            print('----------------------------------')
            print("Iteration: ",i)
            print('Word: ', word)
            print('Current Key: ',curr_key)
            print('Current Value: ',curr_value)
            print('Next Key: ', next_key)
            print('----------------------------------\n')
         

            if (curr_key == 'Name'):
                dict_main[curr_key] = curr_value
                if (next_key in self._target_classes):
                    is_attribute = True
                continue

            if (curr_key in self._target_titles):
                if (next_key is self._target_titles): 
                    print(f"ERROR: <{curr_key}> and <{next_key}> is pointing at target titles.")
                    return
                else:
                    this_key=curr_key
                    this_value=curr_value
                    continue

            elif is_attribute:
                this_key = 'Attribute'
                this_value=curr_value
                is_attribute=False
 
            d_lab[curr_key]+=1
 
            if next_key == " ":
                is_end=True
                
            if ((next_key in self._target_titles) or is_end):
           
        
                tot_adv = (d_lab['Buff']-d_lab['Nerf']) + (d_lab['New']-d_lab['Removed'])
                tot_adj = d_lab['Rework']+d_lab['Rescale']

                if ((tot_adv-tot_adj)>0):
                    verdict='Buff'
                elif ((tot_adv-tot_adj)<0):
                    verdict='Nerf'
                elif (tot_adj==tot_adv):
                    verdict='Adjust'

                dict_stage[this_value] = verdict
                dict_main[this_key]=dict_stage

                for classes in d_lab:
                    d_lab[classes]=0

                this_key,this_value='',''

            if is_end:

                is_end = False
                with open("DATASET.json", 'a') as j:
                    json.dump(dict_main, j, indent=2)
                    
                dict_main.clear()
                dict_stage.clear()
    
                for classes in d_lab:
                    d_lab[classes]=0

                this_key,this_value='',''
    
                continue

    def get_patch_notes (self):

        patch_stage=[]
        patch_final=[]
      
        soup = self.get_html()
        hero_start = soup.find('span',{'id': self._h2_hero_id})
        all_h3 = hero_start.find_all_next('h3')
 
        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):

                fixed_h3 = h3.text.replace("[edit]","").strip()
                fixed_h3  = "Name,"+fixed_h3
                patch_stage.append(fixed_h3)

                ul_container = h3.find_next('ul')
                all_li = ul_container.find_all('li')

                for i,li in enumerate(all_li):
             
                    in_line = li.find('b')

                    if (in_line):

                        if (in_line.text.strip() == "Talent"):
                            title = "Talent"
                        else:
                            title = "Skill"

                        patch_stage.append( f"{title}," + in_line.text.strip())
                
                    else:
                        patch_class = li.find('img',alt=lambda value: value in self._target_classes)
                        if (patch_class):
                            patch_stage.append(f"{patch_class.get('alt')},"+li.text.strip())

         
                patch_stage.append(" ")
            
                if (not(self.__check_eol(patch_stage))):
                    patch_final += patch_stage
                else:
                    continue

                patch_stage.clear()

        return patch_final
    
    




patches = ["7.34","7.34b","7.34c","7.34d","7.34e","7.35"]
# patches = ["7.34"]



obj = DatasetBuilder("7.35")
patch_list = obj.get_patch_notes()
obj.mekus(patch_list)




 
