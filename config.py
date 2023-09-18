import json

with open('config/settings.json', 'r', encoding='utf8') as jFile:
    data = json.load(jFile)

with open('config/cell_war.json', 'r', encoding='utf8') as jFile:
    cwconfig = json.load(jFile)

def get_configs(category = None):
    if category == "cw":
        return cwconfig
    return data
    
def get_config(key: str, category = None):
    if category == "cw":
        return cwconfig[key]
    return data[key]