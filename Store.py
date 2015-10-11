__author__ = 'abkhanna'

from pymongo import MongoClient

def database():
    client = MongoClient("mongodb://heroku_pw3tw66l:f6u3bvhehp4es6u4emoo23snol@ds035137.mongolab.com:35137/heroku_pw3tw66l")
    db = client.heroku_pw3tw66l
    return db

class Question:
    @staticmethod
    def put(key, data):
        doc = {
            '_id': str(key),
        }
        doc.update(key.getKeyParts())
        doc.update(data)
        return database().Question.update({'_id': str(key)}, doc, upsert=True)

    @staticmethod
    def fetch(questionUrn):
        return database().Question.find({'question_urn': questionUrn})

    @staticmethod
    def get(key):
        return database().Question.find({'_id': str(key)})[0]

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

    @staticmethod
    def fetchByEmail(emailAddress):
        return database().Contact.find({'emailAddress': str(emailAddress)})
