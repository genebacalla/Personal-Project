from bs4 import BeautifulSoup
import requests
import time
import json
import xmltodict
import os 

class DatasetBuilder:

    subhead = ['Buff',"Nerf","New","Rework","Rescale","Removed","Rework"]
    header_hero = ['Heroes','Hero_Updates']
    headers = ['Attribute','Talent','Skill']
    

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
        
    def build_json(self,patch):
        main={}
        frame=[]
        tmp=[]

        for i,(curr,nxt) in enumerate(zip(patch, patch[1:] + [None])):

            curr=curr.split(',')

            if curr[0]=='Name':
                main['hero_name']=curr[1]
                continue

            if (curr[0] in self.headers):
                tmp.clear()
                tmp.append(self._get_note(i,patch))
            
                if curr[0] in main.keys():
                    main[curr[0]].extend(tmp.copy())
                    
                else:
                    main[curr[0]]=(tmp.copy())
           
            elif curr[0] == " ":
                frame.append(main.copy())
                main.clear()

            if nxt == None:
                 with open("DATASET.json", 'a') as j:
                    for dicts in frame:
                        json.dump(dicts, j, indent=1)
                    


            
    def _get_note(self,i,patch):
        dict={}

        line=patch[i].split(',')
        if line[0] == 'Skill':
            dict['skill_name']=line[1]
        
        for word in patch:
            word=patch[i+1].split(',')

            if (word[0] in self.subhead):
                dict[word[1]]=word[0]
                i+=1	
            else:
                return dict
            
    def parser(self,h3,list):

        patch_stage=list
        uls = h3.find_next('ul')
        lis = uls.find_all('li')
        has_title = False

        for li in lis:
            in_line = li.find('b')
            
            if (in_line):
                has_title=True
                if (in_line.text.strip() == "Talent"):
                    title = "Talent"
                else:
                    title = "Skill"

                patch_stage.append( f"{title}," + in_line.text.strip())
        
            else:
                patch_class = li.find('img',alt=lambda value: value in self.subhead)
                
                if not(has_title) and patch_class:
                    patch_stage.append('attribute,'+'attribute')
                    has_title=False

                if (patch_class):
                    patch_stage.append(f"{patch_class.get('alt')},"+li.text.strip())

        patch_stage.append(' ')
        return patch_stage


    def get_patch_notes (self):

        patch_stage=[]
        patch_final=[]
      
        soup = self.get_html()
        hero_start = soup.find('span',{'id': self.header_hero})
        all_h3 = hero_start.find_all_next('h3')
 
        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):

                patch_stage.append("Name,"+h3.text.replace("[edit]","").strip())
                patch_final = self.parser(h3,patch_stage)

        
        return patch_final
    
    

patches = ["7.34","7.34b","7.34c","7.34d","7.34e","7.35"]
# patches = ["7.34"]



obj = DatasetBuilder("7.35")
patch_list = obj.get_patch_notes()
obj.build_json(patch_list)




 
