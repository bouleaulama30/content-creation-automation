import csv
import dotenv
import os
import requests as r
import random as rd
import json

dotenv.load_dotenv()

DATA_CLIENT_FILE = os.getenv('DATA_CLIENT_FILE')
LINKS_VIRAL_FILE_PATH = os.getenv('LINKS_VIRAL_FILE_PATH')
URL = os.getenv('URL')

with open(f"{DATA_CLIENT_FILE}", 'r') as json_data:
    data = json.load(json_data)
LANG = data.get('LANG', 'fr')


url = f"{URL}:5000/test"

def send_server_request(url, data_client, timeout):
    try:
        r.post(url, json=data_client, timeout=timeout)
    except r.exceptions.Timeout:
        print("timeout")
        

def select_random_line(input_file):
    with open(input_file, 'r') as f:
        csv_lines = csv.reader(f)
        lines_list = [row for row in csv_lines]
    rd.shuffle(lines_list)
    return lines_list[0]

def create_data_client(link, template, script_number, word_number, lang):
    data_client = {
            'link': link,
            'template': template,
            'LANG': lang,
            'addLinkPool': False,
            'createFromLinkPool': False,
            'createOriginalContent': False,
            'createScriptFromViralLinkPool': False,
            'createScriptFromLink': True,
            'createScriptFromInput': '',
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    return data_client

def get_script_parameters(input_json_file):
    with open(input_json_file, 'r') as json_data:
        data = json.load(json_data)
    return [data['scriptNumber'], data['wordNumber']]

    
if __name__ == "__main__":
    random_csv_line = select_random_line(f"{LINKS_VIRAL_FILE_PATH}/viral-links-{LANG}.csv")
    script_parameters = get_script_parameters(f"{DATA_CLIENT_FILE}")
    data_client = create_data_client(random_csv_line[0], random_csv_line[1], script_parameters[0], script_parameters[1], LANG)
    print(data_client)
    send_server_request(url, data_client, 3)
    
