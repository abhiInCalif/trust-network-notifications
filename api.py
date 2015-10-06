__author__ = 'abkhanna'

import web
import channels

urls = (
    '/notification/create', 'NotificationCreate',
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




# to run the notifications service. Meant to run on another machine ideally.
# if you don't have the manpower to run it on a different system, can just
# import it.
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
