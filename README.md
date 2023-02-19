# Domotique avec commandes vocales et Tkinter sur des Raspberry Pi

Des projets proches des projets Système d'alarme avec un Raspberry Pi: <a href="https://github.com/ugolabo/systeme_alarme_rpi">bouton droit vers repo</a>

1. Projet, v1
2. Projet, v2

## Projet, v1: commandes avec boutons

**Objectif:** maitriser les fondements des nanoordinateurs (Raspberry Pi), des OS Linux (Raspbian, mais aussi Ubuntu, les CLI) et de montages, d'un émulateur Raspberry Pi (RpiSim) pour OS Linux, du langage Python embarqué, de concepts les fils d'exécution (*thread*), des évènements sur le système, de la conception d'interfaces graphiques (avec Tkinter), du protocole MQTT (avec un serveur Mosquitto et le service web MyQTT Hub) pour acheminer les données, colliger les transactions dans une base de données MongoDB pour garder l'historique des commandes et plus afin de construire des projets simples en IoT et de pouvoir collaborer avec des spécialistes de ces domaines dans des projets avancés.

Consulter le README du projet (dans le projet) pour plus de détails. À noter que le fichier cles.py du projet contient des valeurs pour s'authentifier à MyQTT Hub, mais ces valeurs sont factices; il faut les changer.

Gif 1

**Description:** l'interface graphique du 1er Raspberry Pi permet de piloter un 2e Raspberry Pi à distance. Ce dernier pilote des objets connectés. En domotique, les objets peuvent être des lampes (allumer-éteindre), des ventilateurs (allumer-éteindre), des stores (monter-descendre), des portes (ouvrir-fermer ou verrouiller-déverrouiller), un système d'alarme (armer-désarmer), etc. L'interface du 1er Raspberry Pi montre les boutons de commande et les états des objets connectés. L'exécution de chaque commande devient un message MQTT qui passe par le web. Une fois la commande reçue et décodée par le 2e Raspberry Pi, ce dernier change l'état d'un objet (d'allumé à éteint, par exemple). Le 2e Raspberry Pi renvoie une confirmation du changement d'état avec un nouveau message MQTT. Une fois la changement d'état reçu et décodé par le 1er Raspberry Pi, ce dernier change l'affichage de l'état sur l'interface. L'exécution de chaque commande est gardée dans une base de données comme historique.
