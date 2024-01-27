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

    def get_html (self):

        url = f"https://liquipedia.net/dota2/Version_{self.version_patch}"
        resp = requests.get(url)
        html_content = resp.content
        return BeautifulSoup(html_content,'html.parser')
    
    def mekus (self,words):

        buff,nerf,new,rework,rescale,removed=0,0,0,0,0,0
     
        dict_main={}
        dict_attribute={}
        dict_skill={}
        dict_talent={}
        flag_target_title=False
        flag_force_submit=False
        is_attr=False
        this_key= ''
        this_value=''

        # locales = [dict_main,dict_attribute,dict_skill,dict_talent,
        #     flag_force_submit,flag_target_title,flag_skill,flag_talent,flag_attr,
        #     buff,nerf,new,rework,rescale,removed,
        #     this_key,this_value
        #     ]

        flag_attr,flag_skill,flag_talent=False,False,False
        for i,word in enumerate(words):

       
            if (word == " "):
                continue

            _curr_phrase=word.split(',')
            curr_key=_curr_phrase[0]
            curr_value=_curr_phrase[1]
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
                    is_attr = True
                continue


            if (curr_key in self._target_titles):
         
                if (next_key is self._target_titles): 
                    print(f"ERROR: <{curr_key}> and <{next_key}> is pointing at target titles.")
                    return
                else:
                    this_key=curr_key
                    this_value=curr_value
                    continue

            elif (is_attr):
                this_key = 'Attribute'
                this_value=curr_value
       
                is_attr=False
 
            if curr_key == 'Buff':
                buff+=1
            elif curr_key == 'Nerf':
                nerf+=1
            elif curr_key == 'Rescale':
                rescale+=1
            elif curr_key == 'New':
                new+=1
            elif curr_key == 'Rework':
                rework+=1
            elif curr_key == 'Removed':
                removed+=1
          

            if ((next_key == " ") and (not(flag_target_title))):
                ("ERROR: The function is force submitting the current iteration.")
                flag_force_submit=True
                
            if ((next_key in self._target_titles) or (flag_force_submit)):
                flag_target_title = True
                

                total_adv = (buff-nerf) + (new-removed)
                total_adj = rework+rescale

                if ((total_adv-total_adj)>0):
                    verdict='buff'
                elif ((total_adv-total_adj)<0):
                    verdict='nerf'
                elif (total_adj==total_adv):
                    verdict='adjust'
                


                if (this_key == 'Attribute'):
                    dict_attribute[this_value] = verdict
                    flag_attr=True
            
                elif (this_key == 'Skill'):
                    dict_skill[this_value] = verdict
                    flag_skill=True

                elif (this_key == 'Talent'):
                    dict_talent[this_value] = verdict
                    flag_talent=True

      
                buff,nerf,new,rework,rescale,removed=0,0,0,0,0,0
                this_key=''
                this_value=''
                flag_target_title = False
       
            if (next_key == " " or next_key=='\n'):

                print("NOTE: The function is now submitting the main dictionary.")
                
                if flag_attr:
                    dict_main['Attribute']=dict_attribute
                if flag_skill:
                    dict_main['Skill']=dict_skill
                if flag_talent:
                    dict_main['Talent']=dict_talent

    
                with open("DATASET.json", 'a') as j:
                    json.dump(dict_main, j, indent=2)
                    


                dict_main.clear()
                dict_attribute.clear()
                dict_skill.clear()
                dict_talent.clear()
                flag_force_submit = False
                flag_target_title = False
                flag_skill=False
                flag_talent=False
                flag_attr=False

                buff,nerf,new,rework,rescale,removed=0,0,0,0,0,0
                this_key=''
                this_value=''

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




 
