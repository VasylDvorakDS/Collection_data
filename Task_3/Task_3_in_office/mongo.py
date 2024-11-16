

from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import *

client =MongoClient('localhost', 27017)
db=client['users']
#db2=client['books']
persons=db.persons

doc = {
    "appid": 292030,
    "positive": 632627,
    "negative": 25245,

    "name": "The Witcher 3: Wild Hunt",
    "developer": "CD PROJEKT RED",
    "publisher": "CD PROJEKT RED",
    "genre": "RPG",
    "release_date": "2015/05/18",
}

try:
    persons.insert_one(doc)
except DuplicateKeyError as e:
    print(e)

for doc in persons.find():
    print()
    pprint(doc)

#persons.insert_many(doc)
