import json

attr_list = {"Buff":"Base Damage increased to 50."}
skill_list = {"Winter's Curse": "Buff" ,"Cold Embrace":"Buff","Arctic Burn":"Buff"}
talent_list = {"Level 25":"Buff","Level 20":"Buff","Level 15":"Nerf"}
my_variable = {
        "Name:":"Wynter Wyvern",
        "Attributes:": attr_list,
        "Skills": skill_list,
        "Talents": talent_list
}



with open("sample.json", 'w') as j:

    json.dump(my_variable, j, indent=2)