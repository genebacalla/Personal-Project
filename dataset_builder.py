from bs4 import BeautifulSoup
import requests
import time
import json
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
        tmp=[]

        for i,p in enumerate(patch):

            p=p.split(',')

            if p[0]=='Name':
                main['hero_name']=p[1]
                continue

            if (p[0] in self.headers):
                tmp.clear()
                tmp.append(self._get_note(i,patch))
            
                if p[0] in main.keys():
                    main[p[0]].extend(tmp.copy())
                    
                else:
                    main[p[0]]=(tmp.copy())
           
            elif p[0] == " ":
                with open("data.json", 'a') as j:
                    json.dump(main, j, indent=2)
                main.clear()
            
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
                

    def _li_parser(self,h3):

        ul_container = h3.find_next('ul')
        all_li = ul_container.find_all('li')
        has_header = False

        patch=[]

        for i,li in enumerate(all_li):
            in_line = li.find('b')
            
            if (in_line):
                has_header=True
                if (in_line.text.strip() == "Talent"):
                    title = "Talent"
                else:
                    title = "Skill"

                patch.append( f"{title}," + in_line.text.strip())
        
            else:
                patch_class = li.find('img',alt=lambda value: value in self.subhead)
                
                if not has_header and patch_class:
                    patch.append('Attribute,'+'Attribute')
                    has_header=False

                if (patch_class):
                    
                    patch.append(f"{patch_class.get('alt')},"+li.text.strip())

        return patch

    def get_patch_notes (self):

        patch_stage=[]
        patch_final=[]
      
        soup = self.get_html()
        hero_start = soup.find('span',{'id': self.header_hero})
        all_h3 = hero_start.find_all_next('h3')
 
        for i,h3 in enumerate(all_h3):
            
            if (h3.find_next('ul')):
                fixed_h3 = h3.text.replace("[edit]","").strip()
                patch_final.append("Name,"+fixed_h3)
                patch_final.append(self._li_parser(h3))

        return patch_final
    
    




patches = ["7.34","7.34b","7.34c","7.34d","7.34e","7.35"]
# patches = ["7.34"]



obj = DatasetBuilder("7.35")
patch_list = obj.get_patch_notes()
obj.build_json(patch_list)




 
