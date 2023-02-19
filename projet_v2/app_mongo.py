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
pprint(list(db.etats.find({'composant': 'COMP1'})))
pprint(list(db.etats.find({'composant': 'COMP2'})))
pprint(list(db.etats.find({'composant': 'COMP3'})))
pprint(list(db.etats.find({'composant': 'COMP4'})))

res = list(db.etats.find())
print(len(res))

res = list(db.etats.find({'composant': 'COMP1'}))
print(len(res))

res = list(db.etats.find({'composant': 'COMP2'}))
print(len(res))

res = list(db.etats.find({'composant': 'COMP3'}))
print(len(res))

res = list(db.etats.find({'composant': 'COMP4'}))
print(len(res))

# Supprimer les documents
db.etats.delete_many({'composant': 'COMP1'})
db.etats.delete_many({'composant': 'COMP2'})
db.etats.delete_many({'composant': 'COMP3'})
db.etats.delete_many({'composant': 'COMP4'})

# Vérifier les documents dans la collection
pprint(list(db.etats.find()))

# ----------------------------------------------
# ARRÊTER LE SERVEUR mongod
