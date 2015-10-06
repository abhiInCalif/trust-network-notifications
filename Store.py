__author__ = 'abkhanna'

from pymongo import MongoClient

def database():
    client = MongoClient()
    db = client.trustnetwork
    return db

class Member:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        # doc.update(key.getKeyParts()), not needed since currently just phone number key
        doc.update(data)
        return database().Member.update({'_id': str(key)}, doc, upsert=True)

    def fetch(self):
        pass

    @staticmethod
    def get(key):
        cursor_list = list(database().Member.find({'_id': str(key)}))
        return cursor_list[0] if len(cursor_list) > 0 else {}

class Contact:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key)
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Contact.update({'_id': str(key)}, doc, upsert=True)

    @staticmethod
    def fetch(actorUrn):
        return database().Contact.find({'actor_urn': str(actorUrn)})

    @staticmethod
    def get(key):
        cursor_list = list(database().Contact.find({'_id': str(key)}))
        return cursor_list[0] if len(cursor_list) > 0 else {}
