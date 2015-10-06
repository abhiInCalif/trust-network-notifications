__author__ = 'abkhanna'

def createUrn(identifier, uniqueKey):
    return 'urn:tn:' + str(identifier) + ':' + str(uniqueKey)

class ContactKey:
    def __init__(self, actorUrn, memberUrn):
        self.actor_urn = actorUrn
        self.member_urn = memberUrn

    def __str__(self):
        return '/' + self.actor_urn + '/' + self.member_urn

    def getKeyParts(self):
        return {'actor_urn': self.actor_urn, 'member_urn': self.member_urn}

class Contact:
    @staticmethod
    def createKey(actorUrn, memberUrn):
        return ContactKey(actorUrn, memberUrn)