__author__ = 'abkhanna'
import requests
import Store
import StoreUtils
import thread

class Channel:
    def send(self, payload):
        # takes in a payload and sends it along the channel being implemented
        # payload has to have the form of: {text:, recipientToken:, asker_name:, question_urn:,}
        pass


# noinspection PyBroadException
class EmailChannel(Channel):
    def send(self, payload):
        # specifically this payload has a text: recipientUrn: asker_name: and a questionUrn:
        # this function is responsible for resolving the urn to get the name of the recipient
        text = payload.get('text', '')
        recipient_urn = payload.get('recipientUrn', '')
        asker_urn = payload.get('askerUrn', '')
        asker_name = resolveActorUrn(asker_urn, "name")
        question_urn = payload.get('urn', '')
        recipient_name = resolveRecipientUrn(asker_urn, recipient_urn, "name")
        recipient_email = resolveRecipientUrn(asker_urn, recipient_urn, "emailAddress")

        if recipient_email:
            # actually send the message to through email
            requests.post("https://api.mailgun.net/v3/sandbox6959a19ef100472fb32d158553348ead.mailgun.org/messages",
                auth=("api", "key-37a0e041a9b9e58de0f1956618fa850c"),
                data={"from": "TrustNetwork <postmaster@sandbox6959a19ef100472fb32d158553348ead.mailgun.org>",
                      "to": "abhi1994@gmail.com",
                      "subject": recipient_name + ", There is a question from " + asker_name + " awaiting your response!",
                      "text": asker_name + "'s questions is:\n" + text + "\n\nTrustNetwork: To respond to the question hit reply."
                            + "\n\n" + " Ticket #: " + question_urn
            })
        else:
            pass  # can't do anything if they don't have an email.


def resolveRecipientUrn(actor_urn, recipient_urn, key):
    contactKey = StoreUtils.Contact.createKey(actorUrn=actor_urn, memberUrn=recipient_urn)
    recipientData = Store.Contact.get(key=contactKey)
    return recipientData.get(key, '')


def resolveActorUrn(actor_urn, key):
    actorData = Store.Member.get(key=actor_urn)
    return actorData.get(key, '')
