# Domotique avec commandes vocales et Tkinter sur des Raspberry Pi

Des projets proches des projets Système d'alarme avec un Raspberry Pi: <a href="https://github.com/ugolabo/systeme_alarme_rpi">bouton droit vers repo</a>

1. [Projet, v1](#projet-v1-commandes-avec-boutons)
2. [Projet, v2](#projet-v2-ajout-des-commandes-vocales-et-plus)

## Projet, v1: commandes avec boutons

**Objectif:** maitriser les fondements des nanoordinateurs (Raspberry Pi), des OS Linux (Raspbian, mais aussi Ubuntu, les CLI) et de montages, d'un émulateur Raspberry Pi (RpiSim) pour OS Linux, du langage Python embarqué, de concepts les fils d'exécution (*thread*), des évènements sur le système, de la conception d'interfaces graphiques (avec Tkinter), du protocole MQTT (avec un serveur Mosquitto et le service web MyQTT Hub) pour acheminer les données, colliger les transactions dans une base de données MongoDB pour garder l'historique des commandes et plus afin de construire des projets simples en IoT et de pouvoir collaborer avec des spécialistes de ces domaines dans des projets avancés.

Consulter le README du projet (dans le projet) pour plus de détails. À noter que le fichier cles.py du projet contient des valeurs pour s'authentifier à MyQTT Hub, mais ces valeurs sont factices; il faut les changer.

<img src="img/projet_v1.gif" alt="" width="800">

L'interface graphique du 1er Raspberry Pi (app1.py dans la console de gauche) permet de piloter un 2e Raspberry Pi à distance (app2.py dans la console de droite). Ce dernier pilote des objets connectés. En domotique, les objets peuvent être des lampes (allumer--éteindre), des ventilateurs (allumer--éteindre), des stores (monter--descendre), des portes (ouvrir--fermer ou verrouiller--déverrouiller), un système d'alarme (armer--désarmer), etc.

Dans ce projet, aucun objet n'est connecté. Les connexions sont représentées par un émulateur de GPIO qui montre les changements d'état (0V--5V) des broches du 2e Raspberry Pi. L'interface du 1er Raspberry Pi montre les boutons de commande et les états des objets connectés. L'exécution de chaque commande change à la fois l'état de l'objet sur l'interface et devient un message MQTT qui passe par le web.

Une fois la commande reçue par le 2e Raspberry Pi, ce dernier change l'état d'une broche GPIO sur l'émulateur. Si le vrai objet était connecté (physiquement) sur le 2e Raspberry Pi, son état changerait: d'allumé à éteint, par exemple. 





L'exécution de chaque commande est envoyée (via un client) dans une base de données, comme historique. Le serveur de cette base de données est actif dans une 3e console, en arrière-plan. Le fichier du projet app_mongo.py sert à faire des opérations CRUD sur un client de cette base de données.

## Projet, v2: ajout des commandes vocales et plus

**Objectif:** poursuivre avec la programmation embarquée et la programmation orientée objet en Python pour bonifier l'interface graphique (avec Tkinter), l'ajouter d'un bouton pour dicter des commandes vocales et incorporer des données météo récupérées sur le web avec l'API OWM afin de les afficher sur l'interface

Consulter le README du projet pour plus de détails. À noter que le fichier cles.py du projet contient des valeurs pour s'authentifier à MyQTT Hub, mais ces valeurs sont factices; il faut les changer. À noter aussi les fichiers PDF de conjugaison pour varier (tester) les commandes vocales.

<img src="img/projet_v2.gif" alt="" width="800">

Pour une meilleure résolution, télécharger et visualiser le fichier MP4 (adjacent à ce README).

Le 1er Raspberry Pi (app_tkinter.py dans la console de gauche) fonctionne aussi avec des commandes vocales; les mêmes que pour les boutons (allumer-éteindre, armer-désarmer, etc.). Une reconnaissance vocale (via le web) convertit l'oral (d'un micro) en texte. Il existe diverses façons de dicter une commande. Par exemple, dicter l'allumage d'une lampe peut se faire avec différents verbes (ouvrir, allumer, etc.), à différents temps de conjugaison, avec diverses constructions syntaxiques. Bref, il n'y a pas de phrase standard.

Pour standardiser une commande vocale et la faire fonctionner, il faut faire du TALN (*NLP*). La phrase de commande subit des modifications: on enlève les stopwords, on réduit la phrase à des tokens, puis à des lemmes. Un lemme est un mot qui a perdu tout accord ou conjugaison. Les lemmes sont comparés à des ensembles de lemmes pour retrouver une commande existante. Si la commande existe, cette dernière devient un message MQTT.

De plus, une énonciation standard de la commande est retournée sous forme de texte, puis convertie en énonciation orale (sauvegardée en fichier sonore). Si la commande vocale n'existe pas ou n'est pas retrouvée, des instructions indiquent à l'usager de recommencer (de changer sa formulation). Le README du projet indique le genre de commandes vocales qui fonctionnent. Des PDF de conjugaisons permettent de varier les commande encore plus.

Que la commande vocale ou activée avec un bouton, si cette commande marche, un message MQTT est acheminé jusqu'au 2e Raspberry Pi (app_gpio.py dans la console de droite). Cependant, l'affichage de l'état de l'objet ne change pas automatiquement sur l'interface du 1er Raspberry Pi. Il faut une confirmation du vrai changement d'état provenant du 2e Raspberry Pi.

Une fois la commande reçue par le 2e Raspberry Pi, ce dernier change l'état d'une broche GPIO sur l'émulateur. Il se peut que la commande ne passe pas; pour toute sorte de raisons. Si l'état a vraiment changé, le 2e Raspberry Pi renvoie une confirmation du changement avec un nouveau message MQTT. Une fois la changement d'état reçu par le 1er Raspberry Pi, ce dernier change l'affichage de l'état sur l'interface.

La base de données roule toujours en arrière-plan, dans une 3e console. 

L'interface du 1er Raspberry Pi est aussi bonifiée avec l'heure du 1er Rapsberry Pi et des données météo récupérées du web avec l'API OWM au moment où l'application fonctionne.
