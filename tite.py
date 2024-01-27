import json

words = ['Hero',',Abaddon']
_target_classes = ['Buff',"Nerf","New","Rework","Rescale","Removed"]
_target_titles = ['[edit]','[attr]','[talent]','[skill]']

def mekus (words):
	for i,word in enumerate(words):

		buff,nerf,new,rework,rescale,removed=0,0,0,0,0,0

		dict_main={}
		dict_attribute={}
		dict_skill={}
		dict_talent={}


		flag_target_title=False
		flag_force_submit=False
		
		_curr_phrase=word.split(',')
		curr_key=_curr_phrase[0],curr_value=_curr_phrase[1]
		next_key= words[i+1].split(',')[0]


		this_key= ''
		this_value=''

		if (curr_key == 'Name'):
			dict_main[curr_key] = curr_value
			if (next_key in _target_classes):
				is_attr = True
			continue


		if (curr_key in _target_titles):
			if (next_key is _target_titles): 
				print(f"ERROR: <{curr_key}> and <{next_key}> is pointing at target titles.")
				return
			else:
				this_key=curr_key
				this_value=curr_value
				continue

		elif (is_attr):
			this_key = 'Attribute'
			is_attr = False

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
			flag_force_submit=True
			
		if ((next_key in _target_titles) or (flag_force_submit)):
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

		if (next_key == " "):
			
			if flag_attr:
				dict_main['Attribute']=dict_attribute
			if flag_skill:
				dict_main['Skill']=dict_skill
			if flag_talent:
				dict_main['Talent']=dict_talent

			with open("sample.json", 'w') as j:
				json.dump(dict_main, j, indent=2)


			dict_main.clear()
			dict_attribute.clear()
			dict_skill.clear()
			dict_talent.clear()
			flag_force_submit = False
			continue