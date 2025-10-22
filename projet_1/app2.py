import paho.mqtt.client as mqtt
import time
from RPiSim import GPIO
import sys

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

# Paramétrer GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Paramétrer les broches GPIO
LED1 = 15
LED2 = 18
ALARME = 17
GND = 25

# Initialiser les broches GPIO en mode output et en rappel haut
# Note: pour ne pas changer le code de couleur de Tk
# les broches sont en rappel haut (HIGH) et RPiSim les colore en rouge;
# rouge correspond à OFF dans Tk
GPIO.setup(LED1, GPIO.MODE_OUT, initial=GPIO.HIGH)
GPIO.setup(LED2, GPIO.MODE_OUT, initial=GPIO.HIGH)
GPIO.setup(ALARME, GPIO.MODE_OUT, initial=GPIO.HIGH)

# Initialiser une broche GPIO en mode output et en rappel haut
# pour simuler le GND inversé (HIGH)
# Note: pour ne pas changer le code de couleur de Tk
# les broches en rappel bas (LOW) sont colorées en vert par RPiSim;
# vert correspond à ON dans Tk
# Eg: si une LED physique est connectée avec l'anode sur GND et cathode sur LED1,
# lorsque LED1 passe de HIGH à LOW, GND reste à HIGH et la LED physique allume
GPIO.setup(GND, GPIO.MODE_OUT, initial=GPIO.HIGH)

# Recevoir l'état du composant de MyQtt et modifier les états GPIO
# args
# client (voir plus haut)
# userdata ???
# message (voir client.on_message plus bas)
def recevoir_modifier(client, userdata, message):
    # Afficher sont état dans la console
    print("Message reçu:", str(message.payload.decode("utf-8")))
    
    # Décomposer le message reçu
    code = str(message.payload.decode("utf-8")).split(" ")
    #print(code)
    
    # Changer l'état GPIO 
    if (code[-2] == 'LED1') and (code[-1] == 'ON'):
        #print(code)
        GPIO.output(LED1, GPIO.LOW) # ON
    elif (code[-2] == 'LED1') and (code[-1] == 'OFF'):
        #print(code)
        GPIO.output(LED1, GPIO.HIGH)
    
    elif (code[-2] == 'LED2') and (code[-1] == 'ON'):
        #print(code)
        GPIO.output(LED2, GPIO.LOW) # ON
    elif (code[-2] == 'LED2') and (code[-1] == 'OFF'):
        #print(code)
        GPIO.output(LED2, GPIO.HIGH)
    
    elif (code[-2] == 'ALARME') and (code[-1] == 'ON'):
        #print(code)
        GPIO.output(ALARME, GPIO.LOW) # ON
    elif (code[-2] == 'ALARME') and (code[-1] == 'OFF'):
        #print(code)
        GPIO.output(ALARME, GPIO.HIGH)
    else:
        pass

# Démarrer la veille du client MyQtt (plusieurs canaux)
client.loop_start()

# Surveiller l'entête du canal du client MyQtt
# même que client.publish() du côté transmission
client.subscribe("ETAT")
# Déclencher la fonction à la réception de données
client.on_message=recevoir_modifier

# Suivant un temps depuis le début de client.loop_start()...
time.sleep(45)
# ...la veille du client arrête...
client.loop_stop()
# ...le simulateur arrête et...
GPIO.cleanup()
# ...le programme arrête
sys.exit("Fin du programme")
