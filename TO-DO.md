# TO DO

## Selection des video (Python)
* faire un code python qui lit les videos d'un dossier, en choisi de manière random et les place dans un dossier
    * à partir du type de reel que l'on veut faire (oogway, animaux, paysage etc) sélectionne les videos dans le bon dossier et format, et calcule les duration frame de la bonne manière

* clean le code python pour l'écriture dans le dossier (plus besoin de l'alea car une permutation sera dejà prete) 

* mettre des variables d'environnement
* lier la durer des videos entre le python et remotion

## Remotion

* séparer le projet en plusieurs fichier et dossier pour que ça soit plus clean
* clean le code pour remotion (le comprendre aussi)
* faire en sorte de calculer les durations frame de la bonne manière (cf calculate metadata)

## Autres
* faire une orga de dossier et de fichier ou je classe les videos par thème (landscape, animals, master oogway)
* faire un script qui lance les commandes:
    * cd content-creation-automation/
    * python test.py
    * npx remotion render --props=./props.json --out --concurrency=2 --output=/home/leo/tiktok-template/public/video.mp4
    * cd ../tiktok-template/
    * rm public/video.json
    * node sub.mjs public/video.mp4
    * npx remotion render --concurrency=2 


* envoie auto sur mon tel:  
    * faire en sorte que la video s'envoit sur mon tel
    * avec le texte de la description et des #
    * avec la miniature auto aussi