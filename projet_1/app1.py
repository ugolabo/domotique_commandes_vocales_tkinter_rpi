import tkinter as tk
import paho.mqtt.client as mqtt
import datetime
import pymongo
import cles

#####
# Paramétrer MyQtt ici et sur le site web
host          = cles.HOST
# Compte
user_name     = cles.USER_NAME
password      = cles.PASSWORD
# Canal
client_id     = cles.CLIENT_ID
# Autres
port          = 1883
clean_session = True

# Utiliser les paramètres de MyQtt
client = mqtt.Client(client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)
client.connect (host, port)

# Transmettre les états initiaux à MyQtt
post_i = "Tous les composants sont OFF\n" + "-" * 50
print("Message non envoyé:", post_i)

# Envoyer l'état du composant vers MyQtt
def envoyer(post):
    # Envoyer son état avec une entête MyQtt
    # même que client.subscribe() du côté réception
    client.publish("ETAT", str(post))
    # Afficher son état dans la console
    print("Message envoyé:", post)

# Bonifier le message
def bonifier(sansdate):
    marqueur = datetime.datetime.now()
    avecdate = f"{marqueur.strftime('%d-%b-%Y')} {marqueur.strftime('%H:%M:%S')} {sansdate}"
    return avecdate

#####
# Préparer MongoDB
print("ATTENTION: DÉMARRER LE SERVEUR MONGODB AVEC:\nsudo service mongod start && systemctl status mongod")
print("\nÀ la fin: stopper le serveur avec:\nsudo systemctl stop mongod && systemctl status mongod")
print("\nTest MongoDB et veille de réception de messages\n(la veille se termine suivant 45s d'inactivité)\n" + "-"*70)
print("Tests MongoDB (attendre la conclusion)")

# Se connecter sur un client MongoDB
try:
    client_mdb = pymongo.MongoClient("localhost")
except:
    print("Démarrer le serveur MongoDB")

# Créer une bd
try:
    db = client_mdb.app2
    print("BD:", db.name, "(OK)")
except:
    print("Terminer l'application ou attendre la fin;\ndémarrer le serveur MongoDB et redémarrer l'application\n" + "-"*70)

# créer une collection
try:
    collection = db.etats
    print("Collection: ", db.list_collection_names(), "(OK)")
    print("Fin des tests MongoDB...\n" + "-"*70)
except:
    print("Terminer l'application ou attendre la fin;\ndémarrer le serveur MongoDB et redémarrer l'application\n" + "-"*70)

# Créer un dictionnaire pour créer un document MongoDB
def creer_dict(sequence):
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
    # Décomposer le code
    decode = code.split(" ")
    # Créer un dictionnaire pour créer un document
    document = creer_dict(decode)
    # Ajouter le document dans MongoDB
    try:  
        collection.insert_one(document).inserted_id
    except:
        print("Le document n'a pas été ajouter à MongoDB")
        
#####
# Gérer les états des composants dans fen
def led_1_on():
    # Composer le message
    message = "LED1 ON"
    # Préparer le texte pour fen
    txt23.configure(text=message.split(' ')[-1],
                    fg="blue", bg="lightgreen",
                    width=5, justify="center", border=10)
    # Bonifier le message
    message = bonifier(message)
    # Invoquer la fonction pour la ajouter le texte dans fen2
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    # Invoquer la fonction pour transmettre le message à MyQtt
    envoyer(message)
    # Invoquer la fonction pour charger MongoDB
    charger(message)
    

def led_1_off():
    message = "LED1 OFF"
    txt23.configure(text=message.split(' ')[-1],
                    fg="blue", bg="orange",
                    width=5, justify="center", border=10)
    message = bonifier(message)
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    envoyer(message)
    charger(message)

def led_2_on():
    message = "LED2 ON"
    txt53.configure(text=message.split(' ')[-1],
                    fg="blue", bg="lightgreen")
    message = bonifier(message)
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    envoyer(message)
    charger(message)

def led_2_off():
    message = "LED2 OFF"
    txt53.configure(text=message.split(' ')[-1],
                    fg="blue", bg="orange")
    message = bonifier(message)
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    envoyer(message)
    charger(message)

def alarme_armee():
    message = "ALARME ON"
    txt83.configure(text=message.split(' ')[-1],
                    fg="blue", bg="lightgreen")
    message = bonifier(message)
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    envoyer(message)
    charger(message)

def alarme_off():
    message = "ALARME OFF"
    txt83.configure(text=message.split(' ')[-1],
                    fg="blue", bg="orange")
    message = bonifier(message)
    try: ajouter(message)
    except: pass # Le message n'a pas été ajouté
    envoyer(message)
    charger(message)

# Construire sur demande la fenêtre fen2
def afficher():
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
    boite.insert(tk.INSERT, " "*5 + "Date" + " "*8 + "Heure" + " "*4 + "État\n" + "-" * 45 + "\n")
    
    #fen2.tk.eval('tk::PlaceWindow {0} widget {1}'.format(fen2, fen))

# Gérer l'affichage de l'historique dans fen2
# Initialiser le compteur de l'historique
compteur = 0
# Initialiser la décision de supprimer tout l'affichage de l'historique
nettoyeur = False

# Ajouter l'historique
def ajouter(etat):
    global compteur
    global nettoyeur
    global boite
    # Si...
    if nettoyeur == True:
        # ...nettoyer tout l'affichage de l'historique
        boite.delete(1.0, tk.END)
        # Re-débuter l'affichage
        boite.insert(tk.INSERT, " "*5 + "Date" + " "*8 + "Heure" + " "*4 + "État\n" + "-" * 45 + "\n")
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

#####
# Construire la principale fenêtre fen
fen = tk.Tk()
fen.geometry("215x260+75+200")
fen.title("App1")

# Construire chaque ligne du cadre de fen
# max de 5 column
# texte, bouton, zone de texte
# row 0
txt02 = tk.Label(fen, text=" ")
txt02.grid(row=0, column=2)

txt02 = tk.Label(fen, text=" ")
txt02.grid(row=0, column=3)

txt03 = tk.Label(fen, text="État",
                 justify="center")
txt03.grid(row=0, column=4)

# row 1
txt10 = tk.Label(fen, text="LED1")
txt10.grid(row=1, column=1, columnspan=2)

# row 2
bouton20 = tk.Button(fen, text="ON",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=led_1_on) # INVOQUER
bouton20.grid(row=2, column=1)


bouton21 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=led_1_off) # INVOQUER
bouton21.grid(row=2, column=2)

txt23 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt23.grid(row=2, column=4)

# row 3
txt30 = tk.Label(fen, text=" ")
txt30.grid(row=3, column=0)

# row 4
txt40 = tk.Label(fen, text="LED2")
txt40.grid(row=4, column=1, columnspan=2)

# row 5
bouton50 = tk.Button(fen, text="ON",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=led_2_on) # INVOQUER
bouton50.grid(row=5, column=1)

bouton51 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=led_2_off) # INVOQUER
bouton51.grid(row=5, column=2)

txt53 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt53.grid(row=5, column=4)

# row 6
txt60 = tk.Label(fen, text=" ")
txt60.grid(row=6, column=0)

# row 7
txt70 = tk.Label(fen, text="Alarme")
txt70.grid(row=7, column=1, columnspan=2)

# row 8
bouton80 = tk.Button(fen, text="ARMER",
                     fg="white", bg="green", activebackground="lightgreen",
                     justify="center", width=5,
                     command=alarme_armee) # INVOQUER
bouton80.grid(row=8, column=1)

bouton81 = tk.Button(fen, text="OFF",
                     fg="white", bg="red", activebackground="orange",
                     justify="center", width=5,
                     command=alarme_off) # INVOQUER
bouton81.grid(row=8, column=2)

txt83 = tk.Label(fen, text="OFF",
                 fg="blue", bg="orange",
                 width=5, justify="center", border=10)
txt83.grid(row=8, column=4)

# row 9
txt90 = tk.Label(fen, text=" ")
txt90.grid(row=9, column=0)

# row 10
txt100 = tk.Label(fen, text="Historique")
txt100.grid(row=10, column=1, columnspan=2)

# row 11
# Afficher l'état dans l'historique
bouton110 = tk.Button(fen, text="AFFICHER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=10,
                      command=afficher) # INVOQUER
bouton110.grid(row=11, column=1, columnspan=2)

# Activer Tk
fen.mainloop()
