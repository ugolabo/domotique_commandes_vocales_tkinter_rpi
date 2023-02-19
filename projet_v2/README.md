## Installer

### OS

- Le projet a été testé sous un système d'exploitation Ubuntu 20.04 LTS.
- Le projet s'appuie sur des algorithmes. Il faut une connexion Internet pour que ces derniers puissent envoyer et télécharger des données.

### Modules et paramètres

Le projet utilise quelques modules standards et quelques modules indépendants.

- Mosquitto pour le serveur en ligne MyQtt et le module `paho-mqtt`.
    - `sudo apt install mosquitto`
    - https://pypi.org/project/paho-mqtt/
    - `pip install paho-mqtt`
- Comme un compte est déjà actif, le projet devrait fonctionner. Les paramètres sont inclus dans les codes sources.

- MongoDB pour stocker les données et le module `pymongo`.
    - https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
    - https://pypi.org/project/pymongo/
    - `pip install pymongo`

- Un simulateur de Raspberry Pi pour simuler le nanoordinateur sur un PC. Il faut faire du dossier du simulateur un sous-répertoire du répertoire des codes sources.
    - https://github.com/mnpappo/rpisim

- Un algorithme de reconnaissance vocale, `speech_recognition`, pour retranscrire la langue orale.
    - https://pypi.org/project/SpeechRecognition/
    - `pip install SpeechRecognition`
    - Paramètres de la langue: https://cloud.google.com/speech-to-text/docs/languages

- Le projet utilise capte la langue orale avec un microphone branché à l'ordinateur. Ce microphone requiert le module `pyaudio`. Ce dernier est une dépendance de l'algorithme `speech_recognition`. En se limitant au format MP3, on évite un autre module pour traiter le format WAV.
    - https://pypi.org/project/PyAudio/
    - `sudo apt update`
    - `sudo apt install python3-pyaudio`
    - `pip install PyAudio`

- Bibliothèque NLTK (*Natural Language ToolKit*) dédiée en traitement automatique des langues.
    - https://pypi.org/project/nltk/
    - `pip install nltk`
    - Suivant l'installation du module, il faut obtenir les données: un lexique de *tokens* (de mots), dont les *stopwords*. Ces derniers sont tout ce qui n'est pas un nom, un verbe, un adjectif et un adverbe. Par exemple, ce sont des déterminants (le, la, les, l') ou des conjonctions (et, ou, etc.). Il faut lancer les lignes d'instructions suivantes dans un interpréteur Python.

```python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
```

- Pour compléter NLTK, il faut un algorithme pour analyser les phrases, identifier les *tokens*, étiquetter les *tokens* (*POS tags* ou *part-of-speech tags*) (nom, verbe, adjectif, genre, nombre, conjuguaison) et plus encore. Le module `textblob` est un module d'analyse lexicale, mais il est construit pour l'anglais. Le module `textblob_fr` est l'addition francophone de `textblob`; il faut combiner les deux modules.
    - https://pypi.org/project/textblob/
    - https://pypi.org/project/textblob-fr/
    - `pip install textblob textblob-fr`
    - Un lemme (*lemma*) est la racine d'un *token*: la forme infinitive d'un verbe conjugué, la forme sans accord ou sans conjuguaison et sans apostrophe d'un nom, d'un adjectif, d'un déterminant, d'un pronom ou d'un autre *token*.
    - Plusieurs algorithmes peuvent faire ce traitement: TextBlob, WordNet, TreeTagger, Pattern, Gensim et Stanford CoreNLP. En français, la combinaison `textblob` et `textblob_fr` ne fonctionne pas bien pour étiquetter les *tokens*, puis extraire les lemmes. En français, l'algorithme qui fonctionne bien est celui de spaCy.
        - https://pypi.org/project/spacy/
        - https://spacy.io/models/fr
        - `pip install spacy`
    - Suivant l'installation du module, il faut obtenir les données. Selon la documentation, il existe plusieurs corpus.
        - `python -m spacy download fr_core_news_sm`

- Le module `pyowm` pour télécharger des données météorologiques.
    - https://pypi.org/project/pyowm/
    - `pip install pyowm`
    - Paramètres de la langue: https://pyowm.readthedocs.io/en/latest/v3/pyowm-configuration-description.html

- Le module `requests` pour télécharger des fichiers du web (faire des requêtes).
    - https://pypi.org/project/requests/
    - `pip install requests`

- Le module `gtts` permet de faire l'inverse du module `speech_recognition`: convertir à l'oral (sauvegarder un fichier MP3) du texte écrit (une chaine de caractères). Un fichier MP3 de départ accompagne les codes sources.
    - https://pypi.org/project/gTTS/
    - `pip install gTTS`
    - Paramètres de langue: https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang

- Le module `pygame` est nécessaire pour pouvoir écouter un fichier sonore (MP3).
    - https://pypi.org/project/pygame/
    - `pip install pygame`

## Tester

### Répertoire des codes sources

- Le répertoire de travail devrait contenir les codes sources app\_gpio.py, app\_mongo.py et app\_tkinter.py.
- Comme tous les codes sources se trouvent dans le même répertoire, il est important de changer le chemin du répertoire de travail où le fichier app\_tkinter.py se trouve. Cela indique le répertoire par défaut aux autres codes sources.
- Le répertoire comporte aussi un sous-répertoire d'image (img) et le sous-répertoire RPiSim (le simulateur).

### Codes sources

- Certaines lignes de code sont facultatives. Elles sont en commentaire multiligne. Comme le reste du code source, il est possible de les exécuter par sélection (une ligne ou un bloc de lignes).
- Sinon, le code source app\_.py peut être exécuter au complet. Une fenêtre d'instructions suivra.

### Préparation

- Ouvrir trois consoles bash (dont les invites de commande pointent vers le répertoire de travail). Chaque console lance un code source ou une commande.

### Utilisation

- Lancer le serveur MongoDB avec `sudo service mongod start && systemctl status mongod` dans la première console et s'assurer qu'il est **actif**.
- Lancer le code source app\_tkinter.py dans la deuxième console.
    - Une fenêtre de commandes s'ouvre.
- Lancer le code source app\_gpio.py dans la troisième console.
    - Une fenêtre de commandes s'ouvre.
    - Une fenêtre RPiSim s'ouvre pour simuler les broches d'un Raspberry Pi (noter les broches actives surlignées en couleur)
- Utiliser les boutons de l'app\_tkinter.py pour changer les états des composants.
    - Les boutons de l'app\_tkinter.py pilotent les broches du simulateur Raspberry Pi (RPiSim) de l'app\_gpio.py.
- Constater la transmission des messages de changements d'état entre les deux app\_.py.
    - Les composants sur lun vrai Raspberry Pi doivent être branchés entre les broches 15, 18, 17, 27 et la broche 25. La broche 25 est à HIGH. Les autres broches aussi. "Allumer" composant signifie que les broches 15, 18, 17 et 27 doivent passer à LOW. La broche 25 est un "ground inversé". Par exemple, si l'anode de la LED est reliée à 25 (HIGH), la cathode à la 15 (HIGH) et que la 15 bascule de HIGH à LOW suivant un changement d'état de OFF à ON, le courant va passer de la 25 à la 15 pour allumer la LED.
- Utiliser le bouton pour afficher les changements d'état (une fenêtre Tkinter (App1 - Historique s'ouvre).
- Arrêter les Apps avec les boutons sur les fenêtre.
- Le bouton de Commande vocale permet de remplacer les boutons.

### Commandes vocales possibles

- Ouvrir la lumière de l’entrée. ok
- Fermer la lumière de l’entrée. ok
- Ouvrir la lumière du salon. ok
- Fermer la lumière du salon. ok
- variantes:
    - ouvrir, allumer et conjugaisons (ouvre, j'ouvre, ouvrirais-tu, etc.)
    - fermer, éteindre et conjugaisons
    - lumière, del, lampe, luminaire, éclairage et accords (les lumières, les luminaires, etc.) 
    - entrée, hall et accords
- Ouvrir la porte de l'entrée. ok
- Fermer la porte de l'entrée. ok
- Ouvrir la porte du salon. sans effet???
- Fermer la porte du salon. sans effet???
- Armer l'alarme. ok
- Désarmer l'alarme. ok
- variantes:
    - armer, activer, désarmer, désactiver
- Quelle heure est-il? ok
- Il est quelle heure? ok
- variantes:
    - être et conjugaisons (il serait, il sera, etc.)
    - heure, temps (si employé avec être)
- Quel temps fait-il? ok
- variante:
    - faire et conjugaisons (il ferait, il fera, etc.)
    - temps (si employé avec faire), température, météo

### Extraction

- Les transmissions de l'App1 sont enregistrées dans une base de données et une collection de MongoDB.
- Le code source `app\_mongo.py` offre des lignes de code pour se brancher à la base de données, à la collection et pour faire des extractions.
- **Il n'est pas conseiller** de lancer le code source dans une des consoles ouvertes parce que certaines lignes de code à la fin sont prévues pour **supprimer les données**.
- Il vaut mieux ouvrir le code source dans un éditeur qui permet d'exécuter des parties du code source ou de commenter les lignes `db.etats.delete_many()` et d'autres lignes avant d'exécuter un code source partiel
