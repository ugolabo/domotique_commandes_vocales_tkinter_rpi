# Projet 2

## Mise en place et structure

- Bonification du projet 1. Le projet s'appuie sur des algorithmes de restranscription de la voix. Il faut une connexion Internet pour que ces derniers puissent envoyer et télécharger des données.

- Un algorithme de reconnaissance vocale, `speech_recognition`, pour retranscrire la langue orale.
    - https://pypi.org/project/SpeechRecognition/
    - `pip install SpeechRecognition`
    - Paramètres de la langue: https://cloud.google.com/speech-to-text/docs/languages

- Le projet capte la langue orale avec un microphone branché à l'ordinateur. Ce microphone requiert le module `pyaudio`. Ce dernier est une dépendance de l'algorithme `speech_recognition`. En se limitant au format MP3, on évite un autre module pour traiter le format WAV.
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

- Pour compléter NLTK, il faut un algorithme pour analyser les phrases, identifier les *tokens*, étiquetter les *tokens* (*POS tags* ou *part-of-speech tags*) (nom, verbe, adjectif, genre, nombre, conjuguaison) et plus encore. Le module `textblob` est un module d'analyse lexicale, mais il est construit pour l'anglais. Le module `textblob_fr` est l'addition francophone de `textblob` ; il faut combiner les deux modules.
    - https://pypi.org/project/textblob/
    - https://pypi.org/project/textblob-fr/
    - `pip install textblob textblob-fr`
    - Un lemme (*lemma*) est la racine d'un *token*: la forme infinitive d'un verbe conjugué, la forme sans accord ou sans conjuguaison et sans apostrophe d'un nom, d'un adjectif, d'un déterminant, d'un pronom ou d'un autre *token*.
    - Plusieurs algorithmes peuvent faire ce traitement : TextBlob, WordNet, TreeTagger, Pattern, Gensim et Stanford CoreNLP. En français, la combinaison `textblob` et `textblob_fr` ne fonctionne pas bien pour étiquetter les *tokens*, puis extraire les lemmes. En français, l'algorithme qui fonctionne bien est celui de spaCy.
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

## Organisation du répertoire et exécution

- Le répertoire de travail devrait contenir les codes sources 'app_gpio.py', 'app_mongo.py' et 'app_tkinter.py'.
- Comme tous les codes sources se trouvent dans le même répertoire, il est important de changer le chemin du répertoire de travail où le fichier 'app_tkinter.py' se trouve. Cela indique le répertoire par défaut aux autres codes sources.
- Le répertoire comporte aussi un sous-répertoire d'image ('img') et le sous-répertoire 'RPiSim' (le simulateur).
- Certaines lignes de code sont facultatives. Elles sont en commentaire multiligne. Comme le reste du code source, il est possible de les exécuter par sélection (une ligne ou un bloc de lignes).
- Sinon, les codes sources 'app_.py' peuvent être exécutés au complet. Une fenêtre d'instructions suivra.

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
