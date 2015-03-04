import pymongo
from pymongo import MongoClient

client = MongoClient()

print client.db.collection_names()

myherodb = client.db.myhero

test_data = {   "type": "story",
    "detail": {
        "category": "aids",
        "name": "Aids kills people",
        "content": [
            {   "kind": "text",
                "text": "Aids is very dangerous"
            },
            {   "kind": "text",
                "text": "Aids kills millions of people every year"
            }
        ]
    }
}

new_id = myherodb.insert(test_data)
print new_id
