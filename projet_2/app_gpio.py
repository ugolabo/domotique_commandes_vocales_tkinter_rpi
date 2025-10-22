# 1re partie, MyQTT
import cles
import paho.mqtt.client as mqtt
# 2e partie, GPIO
from RPiSim import GPIO
# 3e partie, MyQTT-GPIO
# 4e partie, Tkinter
import tkinter as tk

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

#######################################################################
# 2e partie, GPIO
#######################################################################

# Paramétrer GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Paramétrer les broches GPIO
# Lum de l'entrée 11, Lum du salon 12
# Porte de l'entrée 19, Alarme 17
COMP1 = 11
COMP2 = 12
COMP3 = 18
COMP4 = 17
GND = 25

# Initialiser les broches GPIO en mode output et en rappel haut
# Note: pour ne pas changer le code de couleur de Tk
# les broches sont en rappel haut (HIGH) et RPiSim les colore en rouge;
# rouge correspond à OFF dans Tk
GPIO.setup(COMP1, GPIO.MODE_OUT, initial=GPIO.HIGH)
GPIO.setup(COMP2, GPIO.MODE_OUT, initial=GPIO.HIGH)
GPIO.setup(COMP3, GPIO.MODE_OUT, initial=GPIO.HIGH)
GPIO.setup(COMP4, GPIO.MODE_OUT, initial=GPIO.HIGH)

# Initialiser une broche GPIO en mode output et en rappel haut
# pour simuler le GND inversé (HIGH)
# Note: pour ne pas changer le code de couleur de Tk
# les broches en rappel bas (LOW) sont colorées en vert par RPiSim;
# vert correspond à ON dans Tk
# Eg: si une LED physique est connectée avec l'anode sur GND et cathode sur LED1,
# lorsque LED1 passe de HIGH à LOW, GND reste à HIGH et la LED physique allume
GPIO.setup(GND, GPIO.MODE_OUT, initial=GPIO.HIGH)

#######################################################################
# 3e partie, MyQTT-GPIO
#######################################################################

def recevoir_modifier(client, userdata, message):
    """Recevoir l'état de l'app_tkinter
    et modifier les états GPIO"""
    # Afficher sont état dans la console
    print("app_gpio; message reçu:", str(message.payload.decode("utf-8")))
    # Décomposer le message reçu
    code = str(message.payload.decode("utf-8")).split(" ")
    # Changer l'état GPIO
    if (code[-2] == 'COMP1') and (code[-1] == 'ON'):
        #print(code)
        GPIO.output(COMP1, GPIO.LOW)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP1') and (code[-1] == 'OFF'):
        GPIO.output(COMP1, GPIO.HIGH)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP2') and (code[-1] == 'ON'):
        GPIO.output(COMP2, GPIO.LOW)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP2') and (code[-1] == 'OFF'):
        GPIO.output(COMP2, GPIO.HIGH)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP3') and (code[-1] == 'ON'):
        GPIO.output(COMP3, GPIO.LOW)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP3') and (code[-1] == 'OFF'):
        GPIO.output(COMP3, GPIO.HIGH)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP4') and (code[-1] == 'ON'):
        GPIO.output(COMP4, GPIO.LOW)
        message2 = " ".join(code)
        envoyer(message2)
    elif (code[-2] == 'COMP4') and (code[-1] == 'OFF'):
        GPIO.output(COMP4, GPIO.HIGH)
        message2 = " ".join(code)
        envoyer(message2)


def envoyer(post):
    """"Envoyer l'état de l'app_gpio vers l'app_tkinter"""
    # Envoyer son état avec une entête MyQtt
    # même que client.subscribe() du côté réception
    client.publish("ETAT_GPIO", str(post))
    # Afficher son état dans la console
    print("app_gpio; message envoyé:", post)

# Démarrer la veille du client MyQtt (plusieurs canaux)
client.loop_start()

# Surveiller l'entête du canal du client MyQtt
# même que client.publish() du côté transmission
client.subscribe("ETAT_BTN")
# Déclencher la fonction à la réception de données
client.on_message=recevoir_modifier

#######################################################################
# 4e partie, Tkinter
#######################################################################

def stopper_myqtt():
    """Cesser l'écoute du client MyQtt et
    quitter la fenêtre Tkinter"""
    # Activer le bouton QUITTER
    bouton22['state'] = tk.NORMAL
    # Fermer le simulateur GPIO
    GPIO.cleanup()
    # Cesser la veille du client
    client.loop_stop()

# Construire la fenêtre fen
fen = tk.Tk()
fen.geometry("175x75+575+220")
# Nommer et afficher la barre supérieure (option)
# ou l'enlever complètement (option)
#fen.title("app_gpio")
fen.overrideredirect(1)

# Construire chaque ligne du cadre de fen
# max de 5 column
# texte, bouton, zone de texte
# row 0
txt01 = tk.Label(fen, text=" ")
txt01.grid(row=0, column=0)

txt01 = tk.Label(fen, text=" ")
txt01.grid(row=0, column=1)

txt02 = tk.Label(fen, text=" ")
txt02.grid(row=0, column=2)

txt03 = tk.Label(fen, text=" ")
txt03.grid(row=0, column=3)

# row 1
txt11 = tk.Label(fen, fg="blue", text="Stopper, puis Quitter", justify="left")
txt11.grid(row=1, column=1, columnspan=4, sticky=tk.W)

# row 2
bouton21 = tk.Button(fen, text="STOPPER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=6,
                      command=stopper_myqtt)  # INVOQUER
bouton21.grid(row=2, column=1, columnspan=1)

bouton22 = tk.Button(fen, text="QUITTER",
                      fg="white", bg="grey25", activebackground="gray50", 
                      justify="center", width=6,
                      command=fen.destroy, state=tk.DISABLED)
bouton22.grid(row=2, column=2, columnspan=1)

# Activer Tk
fen.mainloop()
