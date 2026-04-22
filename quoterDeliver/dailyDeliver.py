import requests as r
import json 
from pathlib import Path
import random as rd
import os
import dotenv

dotenv.load_dotenv()
LINKS_FOLDER_PATH = os.getenv('LINKS_FOLDER_PATH') 
ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH = os.getenv('ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH') 
SCRIPT_NUMBER = 1
WORD_NUMBER = 45

def check_content_in_file(path_file):
    file = Path(path_file)
    if file.is_file() and file.stat().st_size > 0:
        return True
    return False

def check_available_content(templates, content_folder_path, type):
    for template in templates:
        if check_content_in_file(f"{content_folder_path}/{template}-{type}.txt"):
            return template
    return False
    
def get_file_parameters_to_use(templates, type_and_path_list):
    rd.shuffle(templates)
    rd.shuffle(type_and_path_list)
    for (type, path) in type_and_path_list:
        template = check_available_content(templates, path, type)
        if template:
            dico = {'file_path': f"{path}/{template}-{type}.txt", 'template': template, 'type': type }
            return dico
    return False

def create_data_client(templates, type_and_path_list, script_number, word_number, script_input):
    file_parameters = get_file_parameters_to_use(templates, type_and_path_list)
    if not file_parameters:
        rd.shuffle(script_input)
        rd.shuffle(templates)
        dico = {
            'link': '',
            'template': templates[0],
            'addLinkPool': False,
            'createFromLinkPool': False,
            'createOriginalContent': False,
            'createScriptFromLink': False,
            'createScriptFromInput': script_input[0],
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    elif file_parameters['type'] == "links":
        # TODO call a function to get link
        return True
    elif file_parameters['type'] == "scripts":
        dico = {
            'link': '',
            'template': file_parameters['template'],
            'addLinkPool': False,
            'createFromLinkPool': False,
            'createOriginalContent': True,
            'createScriptFromLink': False,
            'createScriptFromInput': '',
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    data_client = json.dumps(dico)
    return data_client

        

url = "http://localhost:5000/test"

# templates = ["default", "oogway", "joker"]
templates = ["joker"]
type_and_path_list = [("links", LINKS_FOLDER_PATH), ("scripts", ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH)]
script_input = ["joie", "amour", "famille"]

if __name__ == "__main__":
    print(create_data_client(templates, type_and_path_list, SCRIPT_NUMBER, WORD_NUMBER, script_input))
# try:
#     r.post(url, json = data_client, timeout=2)
# except r.exceptions.Timeout:
#     print("timeout")