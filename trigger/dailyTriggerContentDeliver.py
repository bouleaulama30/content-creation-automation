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

url = "http://localhost:5000/test"
templates = ["default", "oogway", "joker"]
type_and_path_list = [("links", LINKS_FOLDER_PATH), ("scripts", ORIGINAL_CONTENT_SCRIPTS_FOLDER_PATH)]
# templates = ["joker"]
# type_and_path_list = [("links", LINKS_FOLDER_PATH)]
script_input = [
    "famille",
    "amour",
    "joie",
    "depression",
    "espoir",
    "dépendance aux réseaux",
    # Résilience & Force (Vibe Lion / Entraînement)
    "La solitude comme arme", 
    "Travailler dans le silence absolu", 
    "Le sacrifice que personne ne voit", 
    "La différence entre discipline et motivation", 
    "Se relever quand tout le monde te croit mort",
    "Le prix de l'indépendance",

    # Dark Mindset & Vérité (Vibe Joker / Revanche)
    "La trahison de ceux en qui tu avais le plus confiance", 
    "L'hypocrisie des fausses amitiés", 
    "Utiliser le manque de respect comme carburant", 
    "Pourquoi être trop gentil est une faiblesse", 
    "Disparaître et revenir intouchable",
    "Couper les ponts sans aucune explication",

    # Sagesse & Détachement (Vibe Oogway / Stoïcisme)
    "Le pouvoir absolu du silence", 
    "L'art de ne plus rien attendre de personne", 
    "Accepter ce qu'on ne peut pas contrôler", 
    "L'illusion que les autres vont changer", 
    "Trouver la paix dans le chaos",
    "Comprendre que rien n'est permanent",

    # Relations & Douleur (Sujets hyper-viraux)
    "Guérir d'une déception amoureuse sans se venger", 
    "La dépendance affective et comment la tuer", 
    "Le respect de soi avant l'amour des autres", 
    "La loyauté face à l'opportunisme",
    "Le danger de la nostalgie d'une relation toxique"
]

script_input += [
    # 🧠 Psychologie cachée (très viral)
    "Pourquoi tu t'attaches aux mauvaises personnes",
    "Le besoin d'attention déguisé en indépendance",
    "Pourquoi tu sabotages ce qui est bon pour toi",
    "L'addiction au chaos émotionnel",
    "Chercher l'amour chez quelqu’un d’indisponible",
    "Pourquoi tu reviens toujours vers la même personne",
    "Confondre l’intensité avec l’amour",
    "Le plaisir inconscient de souffrir",

    # 💔 Relations toxiques (version deep)
    "Quand quelqu’un t’aime mais te détruit",
    "Rester par peur d’être seul",
    "L'illusion du 'il va changer'",
    "Aimer quelqu’un qui te respecte pas",
    "Les signes que tu es l’option, pas le choix",
    "Donner trop et devenir invisible",
    "Quand le silence devient une punition",
    "La jalousie déguisée en amour",

    # 🪞 Vérités inconfortables
    "Tu n’es pas une bonne personne pour tout le monde",
    "Personne ne pense à toi autant que tu le crois",
    "Tu n’es pas spécial (et pourquoi c’est une bonne chose)",
    "Les gens partent dès que tu ne leur sers plus",
    "Être remplacé plus vite que prévu",
    "Le respect est souvent conditionnel",
    "Tu es aussi le problème dans certaines histoires",

    # 🧊 Détachement & froideur
    "Arrêter de vouloir être compris",
    "Ne plus expliquer tes choix à personne",
    "Devenir émotionnellement indisponible",
    "Observer sans réagir",
    "Apprendre à partir sans bruit",
    "Ne plus répondre, même quand tu veux",
    "Couper sans regret",
    "Se détacher même quand ça fait mal",

    # 🔥 Ego & identité
    "Construire une identité après avoir tout perdu",
    "Qui tu deviens quand plus personne ne te regarde",
    "Le masque que tu portes tous les jours",
    "Jouer un rôle pour être accepté",
    "Se redéfinir après une humiliation",
    "Devenir quelqu’un que ton ancien toi détesterait",
    "Le regard des autres comme prison",

    # ⏳ Temps & regret
    "Regretter une décision trop tard",
    "Perdre des années pour quelqu’un",
    "Réaliser que tu as gaspillé ton potentiel",
    "Comprendre trop tard ce que tu avais",
    "Le moment où tu vois tout clairement",
    "Grandir et perdre des gens",
    "Vieillir sans devenir meilleur",

    # 📱 Monde moderne (très actuel)
    "L’illusion des relations sur les réseaux",
    "Comparer ta vie à des gens fake",
    "Se sentir vide après des heures sur TikTok",
    "Construire une image qui n’est pas toi",
    "Chercher de la validation en ligne",
    "Le faux succès des autres",
    "Dépendre du regard numérique",

    # ⚔️ Mentalité dure (mais originale)
    "Travailler sans reconnaissance",
    "Être invisible pendant des années",
    "Personne ne viendra te sauver",
    "Gagner sans jamais être célébré",
    "Être seul contre tout le monde",
    "Construire quelque chose sans soutien",
    "Avancer même sans motivation réelle",

    # 🧬 introspection profonde
    "Pourquoi tu fuis le silence",
    "Ne pas se reconnaître soi-même",
    "Se mentir pour éviter la réalité",
    "Refuser de voir les signes",
    "Se perdre dans ses propres pensées",
    "Avoir peur de devenir quelqu’un de meilleur",
    "Saboter ses propres chances",

    # 🎭 angles originaux / narratifs
    "Le jour où tu arrêtes de répondre",
    "Le moment exact où tu comprends",
    "Ce que tu penses mais que tu ne dis jamais",
    "Ce que tu ressens à 3h du matin",
    "Quand tu relis les anciens messages",
    "Le silence après une dispute",
    "Le regard qui change tout",
    "Quand tu fais semblant que ça va",

    # 🧨 sujets borderline (très performants)
    "Pourquoi certaines personnes méritent d’être perdues",
    "Arrêter d’être une bonne personne",
    "Utiliser les gens avant qu’ils t’utilisent",
    "Pourquoi l’amour n’est pas toujours une bonne idée",
    "Être heureux sans personne",
    "Ne plus croire en personne",
    "Aimer sans jamais s’attacher"
]


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
            'createScriptFromViralLinkPool': False,
            'createScriptFromLink': False,
            'createScriptFromInput': script_input[0],
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    elif file_parameters['type'] == "links":
        # TODO call a function to get link
        with open(file_parameters['file_path'], 'r') as f:
            link = f.readline()
            link = link.replace("\n","")
        dico = {
            'link': link,
            'template': file_parameters['template'],
            'addLinkPool': False,
            'createFromLinkPool': False,
            'createOriginalContent': False,
            'createScriptFromViralLinkPool': False,
            'createScriptFromLink': False,
            'createScriptFromInput': '',
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    elif file_parameters['type'] == "scripts":
        dico = {
            'link': '',
            'template': file_parameters['template'],
            'addLinkPool': False,
            'createFromLinkPool': False,
            'createOriginalContent': True,
            'createScriptFromViralLinkPool': False,
            'createScriptFromLink': False,
            'createScriptFromInput': '',
            'scriptNumber': script_number,
            'wordNumber': word_number 
        }
    return dico

def send_server_request(url, data_client, timeout):
    try:
        r.post(url, json=data_client, timeout=timeout)
    except r.exceptions.Timeout:
        print("timeout")
        

if __name__ == "__main__":
    data_client = create_data_client(templates, type_and_path_list, SCRIPT_NUMBER, WORD_NUMBER, script_input)
    print(json.dumps(data_client))
    send_server_request(url, data_client, 20)
    if data_client['link'] == '' and data_client['createOriginalContent'] == False:
        data_client = create_data_client(templates, type_and_path_list, SCRIPT_NUMBER, WORD_NUMBER, script_input)
        print(json.dumps(data_client))
        send_server_request(url, data_client, 5)
