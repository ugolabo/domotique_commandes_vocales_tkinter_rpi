# préambule
import os
# 1re partie, MyQtt (fonctions, variables)
import datetime
import cles
import paho.mqtt.client as mqtt
# 2e partie, MongoDB
import pymongo
# 3e partie, Tkinter (fonctions, variables)
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
# 4e partie, reconnaissance vocale
import speech_recognition as sr
# 5e partie, NLP
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import nltk.data
from nltk.corpus import stopwords
import spacy
# 6e partie, météo
from pyowm import OWM
from pyowm.utils.config import get_default_config
import requests
# 7e partie, ensembles de mots
# 8e partie, reconversion orale
from gtts import gTTS
import pygame
# 9e partie, activer les fonctions des parties 4 à 7
# 10e partie, commande vocale
# main, Tkinter (GUI)

#######################################################################
# préambule
#######################################################################

# Déterminer le répertoire de travail
CHEMIN = cles.CHEMIN
os.chdir(CHEMIN)
print(os.getcwd())

#######################################################################
# 1re partie, MyQTT
#######################################################################

# Paramétrer MyQtt ici et sur le site web
HOST          = cles.HOST
# Compte
USER_NAME     = cles.USER_NAME
PASSWORD      = cles.PASSWORD
# Canal
CLIENT_ID     = cles.CLIENT_ID
# Autres
PORT          = 1883
CLEAN_SESSION = True

# Utiliser les paramètres de MyQtt
client = mqtt.Client(client_id=CLIENT_ID, clean_session=CLEAN_SESSION)
client.username_pw_set (USER_NAME, PASSWORD)
client.connect (HOST, PORT)

# Afficher les états initiaux des composants
POST_I = "Tous les composants sont OFF\n" + "-" * 50
print("Message non envoyé:", POST_I)


def envoyer(post):
    """"Envoyer l'état de l'app_tkinter vers l'app_gpio"""
    # Envoyer son état avec une entête MyQtt
    # même que client.subscribe() du côté réception
    client.publish("ETAT_BTN", str(post))
    # Afficher son état dans la console
    print("app_tkinter; message envoyé:", post)


def bonifier(sansdate):
    """Bonifier le message"""
    marqueur = datetime.datetime.now()
    avecdate = f"{marqueur.strftime('%d-%b-%Y')} {marqueur.strftime('%H:%M:%S')} {sansdate}"
    return avecdate


def recevoir_modifier(client, userdata, message):
    """Recevoir l'état de l'app_gpio vers l'app_tkinter"""
    # Afficher sont état dans la console
    print("app_tkinter; message reçu:", str(message.payload.decode("utf-8")))
    # Décomposer le message reçu
    code = str(message.payload.decode("utf-8")).split(" ")
    # Changer l'état du voyant
    if (code[-2] == 'COMP1') and (code[-1] == 'ON'):
        gerer_voyant(txt24, code[-1])
    elif (code[-2] == 'COMP1') and (code[-1] == 'OFF'):
        gerer_voyant(txt24, code[-1])
    elif (code[-2] == 'COMP2') and (code[-1] == 'ON'):
        gerer_voyant(txt54, code[-1])
    elif (code[-2] == 'COMP2') and (code[-1] == 'OFF'):
        gerer_voyant(txt54, code[-1])
    elif (code[-2] == 'COMP3') and (code[-1] == 'ON'):
        gerer_voyant(txt84, code[-1])
    elif (code[-2] == 'COMP3') and (code[-1] == 'OFF'):
        gerer_voyant(txt84, code[-1])
    elif (code[-2] == 'COMP4') and (code[-1] == 'ON'):
        gerer_voyant(txt114, code[-1])
    elif (code[-2] == 'COMP4') and (code[-1] == 'OFF'):
        gerer_voyant(txt114, code[-1])


def gerer_voyant(label, texte):
    if texte == "ON":
        couleur = "lightgreen"
    else:
        couleur = "orange"
    label.configure(text=texte,
                    fg="blue", bg=couleur,
                    width=5, justify="center", border=10)


# Démarrer la veille du client MyQtt (plusieurs canaux)
client.loop_start()

# Surveiller l'entête du canal du client MyQtt
# même que client.publish() du côté transmission
client.subscribe("ETAT_GPIO")
# Déclencher la fonction à la réception de données
client.on_message=recevoir_modifier

#######################################################################
# 2e partie, MongoDB
#######################################################################

# Préparer MongoDB
print("ATTENTION: DÉMARRER LE SERVEUR MONGODB AVEC:\
      \nsudo service mongod start && systemctl status mongod")
print("\nÀ la fin: stopper le serveur avec:\
      \nsudo systemctl stop mongod && systemctl status mongod")
print("\nTest MongoDB et veille de réception de messages\
      \n(la veille se termine suivant 45s d'inactivité)\n" + "-"*70)
print("Tests MongoDB (attendre la conclusion)")

# Se connecter sur un client MongoDB
try:
    client_mdb = pymongo.MongoClient("localhost")
except Exception:
    print("Démarrer le serveur MongoDB")

# Créer une bd
try:
    db = client_mdb.app2
    print("BD:", db.name, "(OK)")
except Exception:
    print("Terminer l'application ou attendre la fin;\
          \ndémarrer le serveur MongoDB et redémarrer l'application\n" + "-"*70)

# créer une collection
try:
    collection = db.etats
    print("Collection: ", db.list_collection_names(), "(OK)")
    print("Fin des tests MongoDB...\n" + "-"*70)
except Exception:
    print("Terminer l'application ou attendre la fin;\
          \ndémarrer le serveur MongoDB et redémarrer l'application\
              \n" + "-"*70)


def creer_dict(sequence):
    """Créer un dictionnaire pour créer un document MongoDB"""
    # Créer un dictionnaire vide
    doc = {}
    # Remplir le dictionnaire
    for element in sequence:
        doc.update({'date': sequence[0]})
        doc.update({'temps': sequence[1]})
        doc.update({'composant': sequence[2]})
        doc.update({'etat': sequence[3]})
    # Retourner le dictionnaire plein
    return doc

def charger(code):
    """Charger la BD"""
    # Décomposer le code
    decode = code.split(" ")
    # Créer un dictionnaire pour créer un document
    document = creer_dict(decode)
    # Ajouter le document dans MongoDB
    try:
        collection.insert_one(document).inserted_id
    except Exception:
        print("Le document n'a pas été ajouter à MongoDB")

#######################################################################
# 3e partie, Tkinter (fonctions, variables)
#######################################################################

def gerer_composant(nom, etat, label):
    """Gérer les états des composants dans fen"""
    # Composer le message
    message2 = nom + " " + etat
    # Bonifier le message
    message2 = bonifier(message2)
    # Invoquer la fonction pour la ajouter le texte dans fen2
    try: ajouter(message2)
    except Exception: pass # Le message n'a pas été ajouté
    # Invoquer la fonction pour transmettre le message à MyQtt
    envoyer(message2)
    # Invoquer la fonction pour charger MongoDB
    charger(message2)


def gerer_composant_cv(messager):
    """Gérer les états des composants dans fen par commande vocale"""
    message3 = messager
    # Filtrer certains messages (heure, température)
    if len(message3) == 0:
        # Mettre fin à la fonction
        return 0
    # Décomposer le message
    nom, etat = message3.split(" ")
    # Bonifier le message
    message3 = bonifier(message3)
    # Invoquer la fonction pour la ajouter le texte dans fen2
    try: ajouter(message3)
    except: pass # Le message n'a pas été ajouté
    # Invoquer la fonction pour transmettre le message à MyQtt
    envoyer(message3)
    # Invoquer la fonction pour charger MongoDB
    charger(message3)


def afficher():
    """Construire sur demande la fenêtre fen2"""
    fen2 = tk.Toplevel(fen)
    toplevel_offsetx, toplevel_offsety = fen.winfo_x() + fen.winfo_width(), fen.winfo_y()
    padx = 10
    pady = -25
    fen2.geometry(f"322x370+{toplevel_offsetx + padx}+{toplevel_offsety + pady}")
    fen2.title("App1 - Historique")
    # row 0
    txt00 = tk.Label(fen2, text="Renouvellement: QUITTER ou multiple de 20")
    txt00.grid(row=0, column=0)
    # row 1
    global boite
    boite = tk.Text(fen2)
    boite.config(width=45, height=27)
    boite.grid(row=1, column=0)
    # row 2
    txt20 = tk.Label(fen2, text=" ")
    txt20.grid(row=2, column=0)
    # row 3
    bouton30 = tk.Button(fen2, text="QUITTER",
                         fg="white", bg="grey25", activebackground="gray50",
                         justify="center", width=10,
                         command=fen2.destroy) # INVOQUER
    bouton30.grid(row=3, column=0)
    # Débuter l'affichage
    boite.insert(tk.INSERT, " "*5 + "Date" + " "*8 + "Heure" + \
                 " "*4 + "État\n" + "-" * 45 + "\n")


# Gérer l'affichage de l'historique dans fen2
# Initialiser le compteur de l'historique
compteur = 0
# Initialiser la décision de supprimer tout l'affichage de l'historique
nettoyeur = False


def ajouter(etat):
    """Ajouter l'historique"""
    global compteur
    global nettoyeur
    global boite
    # Si...
    if nettoyeur:
        # ...nettoyer tout l'affichage de l'historique
        boite.delete(1.0, tk.END)
        # Re-débuter l'affichage
        boite.insert(tk.INSERT, " "*5 + "Date" + " "*8 + "Heure" + \
                     " "*4 + "État\n" + "-" * 45 + "\n")
    # Augmenter le compteur de l'historique
    compteur += 1
    # Si le compteur est un multiple de 20...
    if (compteur > 0) and (compteur % 20 == 0):
        # Activer le nettoyeur pour la prochaine itération
        nettoyeur = True
    else:
        # Désactiver le nettoyeur pour la prochaine itération
        # Eg: suivant l'itération 20, l'historique affiche 20 états
        # à l'itération 21, l'historique est supprimé pour
        # permettre l'affichage du 21e état et de la suite de l'historique;
        # ainsi de suite suivant 20, 40, 60, etc.
        nettoyeur = False
    # Afficher l'évènement dans l'historique
    boite.insert(tk.INSERT, f" {compteur:02.0f} {etat}\n")  # OUTPUT


def mettre_a_jour_h():
    """Mettre l'heure à jour toutes les 1000ms"""
    heure2 = datetime.datetime.now().strftime("%H:%M:%S")
    txt231.configure(text=f" {heure2} ", justify="center", relief="sunken")
    # récursivité
    fen.after(1000, mettre_a_jour_h)


def stopper_myqtt():
    """Cesser l'écoute du client MyQtt et
    quitter la fenêtre Tkinter"""
    # Activer le bouton QUITTER
    bouton202['state'] = tk.NORMAL
    # Cesser la veille du client
    client.loop_stop()
    
#######################################################################
# 4e partie, reconnaissance vocale
#######################################################################

def lister_microphones():
    """Voir la liste des microphones"""
    try:
        return sr.Microphone.list_microphone_names()
    except Exception as ex:
        return ex


def creer_sr():
    """Créer une instance de reconnaissance vocale"""
    recognizer = sr.Recognizer()
    return recognizer


def ecouter():
    """Capter et enregistrer l'audio avec un microphone"""
    try:
        with sr.Microphone() as source:
            # Paramétrer le "silence" ou le bruit de fond pendant 1s
            print("Attendre 1s........")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Surveille une parole pendant un max de 5s
            # Capter la parole jusqu'au retour du "silence"
            print("Parlez!")
            print("(avant 5s)")
            audio = recognizer.listen(source, timeout=5)
            print("fin")
            return audio
    except Exception:
        return "inaudible, bruit ou rien"


def reconnaitre(aud):
    """Retranscrire l'audio"""
    try:
        parole = recognizer.recognize_google(aud, language="fr-CA")
        return parole
    except Exception:
        return "inaudible, bruit ou rien"

#######################################################################
# 5e partie, NLP
#######################################################################

def creer_tokenizer():
    """Créer une instance de tokenizer
    pour scinder les phrases en tokens"""
    tokenizer = nltk.data.load("tokenizers/punkt/PY3/french.pickle")
    return tokenizer


def analyser_parole(oral):
    """Analyser la retranscription avec le tokenizer"""
    analyse = TextBlob(oral,
                       pos_tagger=PatternTagger(),
                       analyzer=PatternAnalyzer())
    return analyse


def obtenir_stats(ana):
    """Obtenir plus de statistiques sur les tokens"""
    print(ana.words)
    print(ana.sentences)
    # etc.


def charger_lemmes():
    """Charger les données
    pour convertir les tokens en lemmes"""
    nlp = spacy.load("fr_core_news_sm")
    return nlp


def creer_lemmes(ana):
    """Convertir les tokens en lemmes"""
    doc = nlp(str(ana))
    lemmes = []
    for tok in doc:
        # print(token, token.lemma_)
        lemmes.append(tok.lemma_)
    return lemmes


def creer_stopw():
    """Construire une liste de stopwords français"""
    stopw = list(stopwords.words("french"))
    return stopw


def filtrer_lemmes(lem):
    """Filtrer les lemmes pour enlever les stopwords"""
    mots_filtres = []
    for mot in lem:
        if not mot in stopw:
            mots_filtres.append(mot)
    return mots_filtres

#######################################################################
# 6e partie, météo
#######################################################################

def telecharger_owm():
    """Télécharger la météo"""
    config_dict = get_default_config()
    config_dict["language"] = "fr"
    try:
        # Ouvrir une connexion vers OWM
        owm = OWM(cles.owmkey, config_dict)
        mgr = owm.weather_manager()
        # Télécharger les observations
        observation = mgr.weather_at_place("Montreal, CA")
        w = observation.weather
        # Télécharger l'image
        image_meteo = f"http://openweathermap.org/img/wn/{w.weather_icon_name}.png"
        response = requests.get(image_meteo)
        # Sauvegarder l'image
        with open('img/meteo_image.png', 'wb') as fichier:
            fichier.write(response.content)
        return w
    except Exception:
        print("ne peut ouvrir une connexion avec OWM.")

#######################################################################
# 7e partie, ensembles de mots
#######################################################################

class ContruireEnsembles:
    """Créer un constructeur d'ensembles (selon l'algèbre de Venn)"""

    def __init__(self, ens, gram="a"):
        self.ens = ens
        self.gram = gram

    def __str__(self):
        return f"L'ensemble de {self.gram} comprend: {self.ens}"


def compter_phrase():
    """Créer un compteur: phrase
    et un accumulateur: reponse"""
    # Ces trois variables sont récurrentes
    global phrase
    global reponse
    global message
    # sujet, complément, verbe, autre
    phrase = {"s":0, "c": 0, "v": 0,  # 3 critères valant 1 = 3
              "a": 0}                 # 1 critère valant 3 = 3
    reponse = ""  # vide
    message = ""  # vide
    return phrase, reponse, message


def construire_phrase(section):
    """Faire de l'algèbre de Venn (union, intersection, etc.)
    Contruire une reponse avec les lemmes
    'sujet, complément, verbe'
    ou une autre réponse qui remplace 'sujet, complément, verbe'
    Ces trois variables sont récurrentes"""
    global reponse
    global phrase
    global message
    if section == "s":
        if phrase[section] == 0:
            if len(e_objets_lum.ens & e_mots.ens) > 0:
                reponse = reponse + "La lumière "
                phrase[section] = 1
                message = message + "COMPx"
            elif len(e_objets_bui.ens & e_mots.ens) > 0:
                reponse = reponse + "La porte "
                phrase[section] = 1
                message = message + "COMP3"
            elif len(e_objets_sec.ens & e_mots.ens) > 0:
                reponse = reponse + "L'alarme "
                phrase[section] = 1
                phrase["c"] = 1 # 1 auto, car pas de complément nécessaire
                message = message + "COMP4"
            else:
                reponse = reponse + ""
                phrase[section] = 0
                message = message + ""
    if section == "c":
        if phrase[section] == 0:
            if len(e_lieux_1.ens & e_mots.ens) > 0:
                reponse = reponse + "de l'entrée "
                phrase[section] = 1
                message = message.replace("x", "1")
            elif len(e_lieux_2.ens & e_mots.ens) > 0:
                reponse = reponse + "du salon " # aucune porte de salon
                phrase[section] = 1
                message = message.replace("x", "2")
            # Pour l'alarme, répéter de la section précédente
            # L'alarme est générale, sans complément
            elif len(e_objets_sec.ens & e_mots.ens) > 0:
                reponse = reponse + ""
                phrase[section] = 1
                message = message + ""
            else:
                reponse = reponse + ""
                phrase[section] = 0
                message = message + ""
    if section == "v":
        if phrase[section] == 0:
            if len(e_verbes_pos.ens & e_mots.ens) > 0 \
                and len(e_objets_lum.ens & e_mots.ens) > 0:
                reponse = reponse + "est allumée."
                phrase[section] = 1
                message = message + " ON"
            elif len(e_verbes_neg.ens & e_mots.ens) > 0 \
                and len(e_objets_lum.ens & e_mots.ens) > 0:
                reponse = reponse + "est éteinte."
                phrase[section] = 1
                message = message + " OFF"
            elif len(e_verbes_pos.ens & e_mots.ens) > 0 \
                and len(e_objets_bui.ens & e_mots.ens) > 0:
                reponse = reponse + "est ouverte."
                phrase[section] = 1
                message = message + " ON"
            elif len(e_verbes_neg.ens & e_mots.ens) > 0 \
                and len(e_objets_bui.ens & e_mots.ens) > 0:
                reponse = reponse + "est fermée."
                phrase[section] = 1
                message = message + " OFF"
            elif len(e_verbes_pos2.ens & e_mots.ens) > 0 \
                and len(e_objets_sec.ens & e_mots.ens) > 0:
                reponse = reponse + "est armée."
                phrase[section] = 1
                message = message + " ON"
            elif len(e_verbes_neg2.ens & e_mots.ens) > 0 \
                and len(e_objets_sec.ens & e_mots.ens) > 0:
                reponse = reponse + "est désarmée."
                phrase[section] = 1
                message = message + " OFF"
            else:
                reponse = reponse + ""
                phrase[section] = 0
                message = message + ""
    if section == "a":
        if phrase[section] == 0:
            if len(e_variables_tps.ens & e_mots.ens) > 1:
                reponse = f"Il est {datetime.datetime.now().strftime('%H:%M')}."
                phrase[section] = 3
                message = ""
                phrase["s"], phrase["c"], phrase["v"] = 0, 0, 0
            elif len(e_variables_temp.ens & e_mots.ens) > 1:
                reponse = f"Il fait {round(w.temperature('celsius')['temp'], 0)} Celsius."
                phrase[section] = 3
                message = ""
                phrase["s"], phrase["c"], phrase["v"] = 0, 0, 0


def verifier_reponse():
    """Remplacer une réponse incomplète"""
    global reponse
    global phrase
    if sum(list(phrase.values())) < 3:
        reponse = "Je n'ai pas compris. Veuillez recommencer."
        return reponse

#######################################################################
# 8e partie, reconversion orale
#######################################################################

def creer_gtts(rep):
    """Générer l'oral avec l'écrit (text-to-speech)
    et sauvegarder l'oral en MP3"""
    tts = gTTS(rep, lang="fr", tld="ca")
    tts.save(os.getcwd() + "/" + "out.mp3")


def lire_mp3():
    """Lire le fichier MP3"""
    pygame.mixer.init()
    pygame.mixer.music.load(os.getcwd() + "/" + "out.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

#######################################################################
# 9e partie, activer les fonctions des parties 4 à 7
#######################################################################

# Les fonction de la 8e partie sont activées plus loin

# 4e partie, reconnaissance vocale
'''
print(lister_microphones())

# Sélectionner le microphone par défaut du système (ne rien faire)
# ou sélectionner un microphone

# Selon ma liste, la position 4 serait DYNEX USB Audio Device:
sr.Microphone(device_index=4)
'''
recognizer = creer_sr()

# 5e partie, NLP
tokenizer = creer_tokenizer()
nlp = charger_lemmes()
stopw = creer_stopw()
'''
print(stopw)
'''

# 6e partie, météo
w = telecharger_owm()
'''
w.temperature("celsius")
w.pressure
w.wind()
'''
# 7e partie, ensembles de mots
e_verbes_pos = ContruireEnsembles(ens={"allumer", "ouvrir"}, gram="v")
'''
print(e_verbes_pos)
print(e_verbes_pos.ens)
'''
e_verbes_pos2 = ContruireEnsembles(ens={"armer", "activer"}, gram="v")
e_verbes_neg = ContruireEnsembles({"éteindre", "fermer"}, "v")
e_verbes_neg2 = ContruireEnsembles({"désarmer", "désactiver"}, "v")

e_objets_lum = ContruireEnsembles({"lumière", "del", "lampe", "luminaire", "éclairage"}, "s")
e_objets_bui = ContruireEnsembles({"porte"}, "s")
e_objets_sec = ContruireEnsembles({"alarme"}, "s")

e_lieux_1 = ContruireEnsembles({"entrée", "hall"}, "c")
e_lieux_2 = ContruireEnsembles({"salon"}, "c")

e_questions_1 = ContruireEnsembles({"quel"}, "q")
e_verbes_1 = ContruireEnsembles({"être"}, "v")
e_verbes_2 = ContruireEnsembles({"faire"}, "v")
e_variables_tps = ContruireEnsembles({"être", "heure", "temps"}, "a")
e_variables_temp = ContruireEnsembles({"faire", "temps", "température"}, "a")

#######################################################################
# 10e partie, commande vocale
#######################################################################

def passer_cmd_vocale():
    """Passer une commande vocale"""
    # Lancer la boucle à un seul cycle
    while True:
        # 4e partie
        # Réinitialiser les variables
        audio, paroles, analyse = None, None, None
        lemmes, lemmes_filtres = None, None

        # Le cycle est d'un max de 6s
        # 1s pour le 'silence', max de 5s pour la 'parole'
        audio = ecouter()
        '''
        print(audio)
        '''
        paroles = reconnaitre(audio)
        '''
        print(paroles)
        '''
        # Si l'audio n'existe pas, est inaudible,
        # si c'est un bruit de fond,
        # si l'audio ne peut être transcrit en parole,
        # c'est une Exception selon les try plus haut
        # parole reste à None,
        # cesser le cycle
        if paroles == None:
            break
        # Si parole n'est plus None, poursuivre le cycle
        print("paroles:", paroles)

        # 5e partie
        analyse = analyser_parole(paroles)
        '''
        print("analyse:", analyse)
        obtenir_stats("stats:", analyse)
        '''
        lemmes = creer_lemmes(analyse)
        print("lemmes:", lemmes)
        lemmes_filtres = filtrer_lemmes(lemmes)
        print("lemmes filtrés:", lemmes_filtres)

        # 7e partie
        # Cette variable est récurrente
        global e_mots
        e_mots = ContruireEnsembles(ens=set(lemmes_filtres))
        '''
        print(e_mots)
        print(e_mots.ens)
        '''
        # Ces trois variables sont récurrentes
        global reponse
        global phrase
        global message
        phrase, reponse, message = compter_phrase()
        print("réponse préliminaire:", reponse)
        print("somme préliminaire:", sum(list(phrase.values())))
        print("message préliminaire:", message)
        print("début de la construction...")
        i = 0
        for i in ["s", "c", "v", "a"]:
            construire_phrase(i)
            print(reponse)
            print(phrase)
            print(message)
        print("fin de la construction")
        print("réponse à vérifier:", reponse)
        verifier_reponse()
        print("fin de la vérification")
        print("réponse finale:", reponse)
        print("somme finale:", sum(list(phrase.values())))
        print("message final:", message)

        # 8e partie
        creer_gtts(reponse)
        lire_mp3()

        # retour au main (partie)
        gerer_composant_cv(message)
            
        # Terminer la boucle à un seul cycle
        break

#######################################################################
# main, Tkinter (GUI)
#######################################################################

# Construire la principale fenêtre fen
fen = tk.Tk()
fen.geometry("240x650+75+220")
# Nommer et afficher la barre supérieure (option)
# ou l'enlever complètement (option)
#fen.title("app_tkinter")
fen.overrideredirect(1)

# Construire chaque ligne du cadre de fen
# max de 5 column
# texte, bouton, zone de texte
# row 0
txt02 = tk.Label(fen, text=" ")
txt02.grid(row=0, column=2)

txt03 = tk.Label(fen, text=" ")
txt03.grid(row=0, column=3)

txt04 = tk.Label(fen, text="État",
                 justify="center")
txt04.grid(row=0, column=4)

# row 1
txt11 = tk.Label(fen, text="Lumière entrée")
txt11.grid(row=1, column=1, columnspan=2)

# row 2
bouton21 = tk.Button(fen, text="ON",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP1", "ON", txt24)) # INVOQUER
bouton21.grid(row=2, column=1)


bouton22 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP1", "OFF", txt24)) # INVOQUER
bouton22.grid(row=2, column=2)

# condition de départ
txt24 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt24.grid(row=2, column=4)

# row 3
txt30 = tk.Label(fen, text=" ")
txt30.grid(row=3, column=0)

# row 4
txt41 = tk.Label(fen, text="Lumière salon")
txt41.grid(row=4, column=1, columnspan=2)

# row 5
bouton51 = tk.Button(fen, text="ON",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP2", "ON", txt54)) # INVOQUER
bouton51.grid(row=5, column=1)

bouton52 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP2", "OFF", txt54)) # INVOQUER
bouton52.grid(row=5, column=2)

# condition de départ
txt54 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt54.grid(row=5, column=4)

# row 6
txt60 = tk.Label(fen, text=" ")
txt60.grid(row=6, column=0)

# row 7
txt71 = tk.Label(fen, text="Porte entrée")
txt71.grid(row=7, column=1, columnspan=2)

# row 8
bouton81 = tk.Button(fen, text="ON",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP3", "ON", txt84)) # INVOQUER
bouton81.grid(row=8, column=1)

bouton82 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP3", "OFF", txt84)) # INVOQUER
bouton82.grid(row=8, column=2)

# condition de départ
txt84 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt84.grid(row=8, column=4)

# row 9
txt90 = tk.Label(fen, text=" ")
txt90.grid(row=9, column=0)

# row 10
txt101 = tk.Label(fen, text="Alarme")
txt101.grid(row=10, column=1, columnspan=2)

# row 11
bouton111 = tk.Button(fen, text="ARMER",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP4", "ON", txt114)) # INVOQUER
bouton111.grid(row=11, column=1)

bouton112 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=lambda:gerer_composant("COMP4", "OFF", txt114)) # INVOQUER
bouton112.grid(row=11, column=2)

# condition de départ
txt114 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt114.grid(row=11, column=4)

# row 12
txt120 = tk.Label(fen, text=" ")
txt120.grid(row=12, column=0)

# row 13
txt131 = tk.Label(fen, text="Commande vocale")
txt131.grid(row=13, column=1, columnspan=2)

# row 14
bouton141 = tk.Button(fen, text="PARLER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=10,
                      command=passer_cmd_vocale) # INVOQUER
bouton141.grid(row=14, column=1, columnspan=2)

# row 15
txt150 = tk.Label(fen, text=" ")
txt150.grid(row=15, column=0)

# row 16
txt161 = tk.Label(fen, text="Historique")
txt161.grid(row=16, column=1, columnspan=2)

# row 17
bouton171 = tk.Button(fen, text="AFFICHER",
                      fg="white", bg="grey25", activebackground="gray50",
                      justify="center", width=10,
                      command=afficher) # INVOQUER
bouton171.grid(row=17, column=1, columnspan=2)

# row 18
txt180 = tk.Label(fen, text=" ")
txt180.grid(row=18, column=0)

# row 19
txt191 = tk.Label(fen, fg="blue", text="Stopper, puis Quitter", justify="left")
txt191.grid(row=19, column=1, columnspan=4, sticky=tk.W)

# row 20
bouton201 = tk.Button(fen, text="STOPPER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=6,
                      command=stopper_myqtt) # INVOQUER
bouton201.grid(row=20, column=1, columnspan=1, sticky=tk.W)

bouton202 = tk.Button(fen, text="QUITTER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=6,
                      command=fen.destroy, state=tk.DISABLED)
bouton202.grid(row=20, column=2, columnspan=1, sticky=tk.E)


separator = ttk.Separator(fen, orient='horizontal')
separator.place(relx=0, rely=0.665, relwidth=0.95, relheight=1)

# row 21
txt210 = tk.Label(fen, text=" \n ")
txt210.grid(row=21, column=0)

# Heure à l'ouverture de la fenêtre
heure = datetime.datetime.now().strftime("%H:%M:%S")

# Mettre à jour l'heure
# récursivité
fen.after(1000, mettre_a_jour_h)

# Météo à l'ouverture de la fenêtre
temperature = round(w.temperature("celsius")["temp"], 0)
humidite = w.humidity
vitesse_vent = round(w.wind(unit="km_hour")["speed"], 0)
couvert_nuageux = w.clouds
precipitations = w.rain

temp = str(temperature) + "C"
humi = str(humidite) + "°"
vent = str(vitesse_vent) + "km/h"
couv = str(couvert_nuageux) + "%"
prec = str(precipitations) + "mm"

img1 = ImageTk.PhotoImage(file='img/meteo_image.png')
img2 = ImageTk.PhotoImage(file='img/logo.png')

# row 22
txt221 = tk.Label(fen, text="Heure", justify="center")
txt221.grid(row=22, column=1, columnspan=1)

txt222 = tk.Label(fen, text="Température", justify="center")
txt222.grid(row=22, column=2, columnspan=3)

# row 23
txt231 = tk.Label(fen, text=f" {heure} ", justify="center", relief="sunken")
txt231.grid(row=23, column=1, columnspan=1)

txt232 = tk.Label(fen, text=f" {temp} ", justify="center", relief="sunken")
txt232.grid(row=23, column=2, columnspan=3)

# row 24
txt240 = tk.Label(fen, text=" ")
txt240.grid(row=24, column=0)

# row 25
txt251 = tk.Label(fen, text="Humidité", justify="center")
txt251.grid(row=25, column=1, columnspan=1)

txt252 = tk.Label(fen, text="Vent", justify="center")
txt252.grid(row=25, column=2, columnspan=3)

# row 26
txt261 = tk.Label(fen, text=f" {humi}", justify="center", relief="sunken")
txt261.grid(row=26, column=1, columnspan=1)

txt262 = tk.Label(fen, text=f" {vent} ", justify="center", relief="sunken")
txt262.grid(row=26, column=2, columnspan=3)

# row 27
txt270 = tk.Label(fen, text=" ")
txt270.grid(row=27, column=0)

# row 28
txt281 = tk.Label(fen, text="Couvert", justify="center")
txt281.grid(row=28, column=1, columnspan=1)

txt282 = tk.Label(fen, text="Précipitations", justify="center")
txt282.grid(row=28, column=2, columnspan=3)

# row 29
txt291 = tk.Label(fen, text=f" {couv} ", justify="center", relief="sunken")
txt291.grid(row=29, column=1, columnspan=1)

txt292 = tk.Label(fen, text=f" {prec} ", justify="center", relief="sunken")
txt292.grid(row=29, column=2, columnspan=3)

# row 30
txt300 = tk.Label(fen, text=" ")
txt300.grid(row=30, column=0)

# row 31
txt311 = tk.Label(fen, image=img1, justify="center", relief="sunken", bg="cyan")
txt311.grid(row=31, column=1, columnspan=1)

txt312 = tk.Label(fen, image=img2, justify="center")
txt312.grid(row=31, column=2, columnspan=3)

# Activer Tk
fen.mainloop()
