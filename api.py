__author__ = 'abkhanna'

import web
import channels
import re
import Store
import requests

urls = (
    '/notification/create', 'NotificationCreate',
    '/notification/reply/', 'NotificationReply',
    '/notification/reply', 'NotificationReply'
)

def get_message_channel(urn):
    message_channels = {
        "question": [channels.EmailChannel()]
    }
    # check what type of urn it is
    # check the table for the message channel implementation that follows
    urnIdentifier = urn.split(":")[2] if len(urn.split(":")) > 2 else "";
    if urnIdentifier == "":
        return []

    return message_channels.get(urnIdentifier, [])

class NotificationCreate:
    def POST(self):
        web.header('Content-type', 'application/json')
        request_input = web.input(urn='', recipientUrn='', askerUrn='', text='')
        urn = request_input.urn
        recipient_urn = request_input.recipientUrn
        asker_urn = request_input.askerUrn
        text = request_input.text
        if urn == "" or recipient_urn == '' or asker_urn == '' or text == '':
            return web.badrequest()

        # pass on to the appropriate MessageChannel Service
        messageChannels = get_message_channel(urn)
        if not messageChannels:
            return web.badrequest()

        # we have a valid message channels
        for c in messageChannels:
            c.send({"recipientUrn": recipient_urn,
                    "askerUrn": asker_urn,
                    "text": text,
                    "urn": urn
            })

class NotificationReply:
    def POST(self):
        data = web.input()
        print data
        dataMapping = transformToDictionary(data)
        if dataMapping:
            dataForRequest = {
                "askerUrn": dataMapping['asker_urn'],
                "actorUrn": dataMapping['actor_urn'],
                "questionUrn": dataMapping['question_urn'],
                "data": {
                    "isYes": dataMapping['isYes'],
                    "isNo": dataMapping['isNo'],
                    "replyText": dataMapping['replyText']
                }
            }
            print "Making request to Trust Network core service"
            requests.post(url="http://" + "trust-network.herokuapp.com" + "/respond/reply", data=dataForRequest)




def transformToDictionary(data):
    # transforms the email into a dictionary with standard keys
    output_data = {}
    email_from_list = re.findall(r'\<([^]]*)\>', data['from'])
    email_from = ''
    if len(email_from_list) > 0:
        email_from = email_from_list[0]

    full_email_body = data['body-plain']
    email_body = data['stripped-text'] # this is the message data that we wanted to deal with....
    regex_match = re.search(r'^Ticket #:.*\\r\\n', full_email_body)
    if regex_match:
        match_string = regex_match.group(0)
        match_string = match_string[len("Ticket #:") + 1:len(match_string) - 3]
        question_urn = match_string
        output_data['question_urn'] = question_urn
        # add the asker_urn data
        question_data = Store.Question.fetch(questionUrn=question_urn)
        if len(question_data) == 0:
            return {} # error case

        asker_urn = question_data.get('asker_urn', '')
        output_data['asker_urn'] = asker_urn
        # if actor_email exists in the system then we use that else, we need to create a dummy id
        contact_data = Store.Contact.fetchByEmail(email_from)
        if len(contact_data) == 0:
            return {} # error case because everybody getting an email from TrustNetwork must be a contact

        actor_urn = contact_data.get('member_urn', '')
        output_data['actor_urn'] = actor_urn
        output_data['replyText'] = email_body
        output_data['isYes'] = "1"
        output_data['isNo'] = "0"

    return output_data


# to run the notifications service. Meant to run on another machine ideally.
# if you don't have the manpower to run it on a different system, can just
# import it.
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
