# DÉMARRER LE SERVEUR mongod
"""
sudo service mongod start && systemctl status mongod
sudo systemctl status mongod
mongo
mongosh
exit
sudo systemctl stop mongod && systemctl status mongod
sudo systemctl restart mongod
sudo systemctl status mongod
"""
# ----------------------------------------------
import pymongo
from pprint import pprint

# Se connecter sur MongoDB
client = pymongo.MongoClient("localhost")

# Passer à la bd app2
db = client.app2
print(db.name)

# Passer à la collection etats
collection = db.etats
print(db.list_collection_names())

# Vérifier les documents dans la collection
pprint(list(db.etats.find()))
pprint(list(db.etats.find().limit(2)))
pprint(list(db.etats.find().limit(20)))
pprint(list(db.etats.find({'composant': 'LED1'})))
pprint(list(db.etats.find({'composant': 'LED2'})))
pprint(list(db.etats.find({'composant': 'ALARME'})))

res = list(db.etats.find())
print(len(res))

res = list(db.etats.find({'composant': 'LED1'}))
print(len(res))

res = list(db.etats.find({'composant': 'LED2'}))
print(len(res))

res = list(db.etats.find({'composant': 'ALARME'}))
print(len(res))

# Supprimer les documents
db.etats.delete_many({'composant': 'LED1'})
db.etats.delete_many({'composant': 'LED2'})
db.etats.delete_many({'composant': 'ALARME'})

# Vérifier les documents dans la collection
pprint(list(db.etats.find()))

# ----------------------------------------------
# ARRÊTER LE SERVEUR mongod